import os
import uuid
import json
import datetime
from typing import List, Optional
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.docstore.document import Document
from app.utils.trace_utils import write_trace
from app.engines.memory_sync import log_tool_usage
from app.tools.tool_wrappers.structured_input_ingestor import structure_input
from chromadb.config import Settings
import chromadb

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
            client_settings = Settings(
                chroma_api_impl="rest",
                chroma_server_host=CHROMA_HOST,
                chroma_server_http_port=CHROMA_PORT
            )

            vectorstore = Chroma.from_documents(
                split_docs,
                OpenAIEmbeddings(),
                collection_name="policygpt",
                client_settings=client_settings
            )
        else:
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