import os
import uuid
import json
import datetime
from typing import List, Optional
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.docstore.document import Document
from app.utils.trace_utils import write_trace
from app.engines.memory_sync import log_tool_usage
from app.tools.tool_wrappers.structured_input_ingestor import structure_input
from chromadb import HttpClient

CHROMA_DIR = os.getenv("CHROMA_DIR", "./local_vector_store")
CHROMA_HOST = os.getenv("CHROMA_SERVER_HOST")
CHROMA_PORT = os.getenv("CHROMA_SERVER_HTTP_PORT", "8000")
USE_REMOTE_CHROMA = CHROMA_HOST is not None

if not USE_REMOTE_CHROMA:
    os.makedirs(CHROMA_DIR, exist_ok=True)

class Tool:
    def validate(self, input_dict):
        if not input_dict.get("file_contents"):
            raise ValueError("File contents are required")

    def run_tool(self, input_dict):
        self.validate(input_dict)
        file_contents = input_dict["file_contents"]
        file_name = input_dict.get("file_name")
        metadata = input_dict.get("metadata", {})

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        document = Document(page_content=file_contents)
        split_docs = text_splitter.split_documents([document])

        for doc in split_docs:
            doc.metadata.update(metadata)

        if USE_REMOTE_CHROMA:
            client = HttpClient(host=CHROMA_HOST, port=int(CHROMA_PORT))
            collection = client.get_or_create_collection("policygpt")
            collection.add(
                documents=[doc.page_content for doc in split_docs],
                metadatas=[doc.metadata for doc in split_docs],
                ids=[str(uuid.uuid4()) for _ in split_docs]
            )
        else:
            from langchain_community.vectorstores import Chroma
            vectorstore = Chroma.from_documents(split_docs, OpenAIEmbeddings(), persist_directory=CHROMA_DIR)
            vectorstore.persist()

        summary = f"{file_name} with {len(split_docs)} chunks embedded."

        entry = structure_input(file_contents, file_name, tool_name="loadCorpus", metadata=metadata)
        out_path = write_trace(entry)

        log_tool_usage(
            entry["tool"],
            entry["input_summary"],
            json.dumps(summary, indent=2),
            session_id=entry.get("session_id"),
            user_id=entry.get("user_id"),
            metadata=entry.get("metadata")
        )

        return {"status": "success", "path": out_path, "chunks": len(split_docs)}