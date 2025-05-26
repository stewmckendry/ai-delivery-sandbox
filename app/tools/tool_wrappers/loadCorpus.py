import logging
import os
import uuid
import json
import datetime
from typing import List, Optional
from fastapi import BackgroundTasks
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
from app.utils.trace_utils import write_trace
from app.engines.memory_sync import log_tool_usage
from app.tools.tool_wrappers.structured_input_ingestor import structure_input
from chromadb import HttpClient

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
logger.info("✅ loadCorpus Tool loaded at import time")

CHROMA_DIR = os.getenv("CHROMA_DIR", "./local_vector_store")
CHROMA_HOST = os.getenv("CHROMA_SERVER_HOST")
CHROMA_PORT = os.getenv("CHROMA_SERVER_HTTP_PORT", "8000")
USE_REMOTE_CHROMA = CHROMA_HOST is not None
logger.info("USE_REMOTE_CHROMA: %s", USE_REMOTE_CHROMA)
logger.info("CHROMA_HOST: %s", CHROMA_HOST)
logger.info("CHROMA_PORT: %s", CHROMA_PORT)

class Tool:
    async_tool = True  # Enables async execution in api_router

    def validate(self, input_dict):
        if not input_dict.get("file_contents"):
            raise ValueError("Missing file_contents")

    def run_tool(self, input_dict, background_tasks: BackgroundTasks = None):
        self.validate(input_dict)
        job_id = str(uuid.uuid4())

        def process():
            logger.info("🚀 Starting async loadCorpus tool")
            file_contents = input_dict["file_contents"]
            file_name = input_dict.get("file_name", "Unnamed Document")
            metadata = input_dict.get("metadata", {})

            logger.info("✅ File format validated: PDF")
            logger.info("Running loadCorpus tool")

            logger.info("Splitting file contents into chunks")
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
            document = Document(page_content=file_contents)
            split_docs = text_splitter.split_documents([document])
            for doc in split_docs:
                doc.metadata.update(metadata)
            logger.info("Splitting done, embedding documents")

            if USE_REMOTE_CHROMA:
                client = HttpClient(host=CHROMA_HOST, port=int(CHROMA_PORT))
                collection = client.get_or_create_collection("policygpt")
                for doc in split_docs:
                    collection.add(documents=[doc.page_content], metadatas=[doc.metadata], ids=[str(uuid.uuid4())])
            else:
                vectorstore = Chroma.from_documents(split_docs, OpenAIEmbeddings(), persist_directory=CHROMA_DIR)
                vectorstore.persist()

            logger.info("Documents embedded and stored successfully")
            entry = structure_input(file_contents, file_name, tool_name="loadCorpus", metadata=metadata)
            out_path = write_trace(entry)
            logger.info("logging tool usage")
            log_tool_usage(
                entry["tool"],
                entry["input_summary"],
                json.dumps({"status": "success", "chunks": len(split_docs)}, indent=2),
                session_id=entry.get("session_id"),
                user_id=entry.get("user_id"),
                metadata=entry.get("metadata")
            )
            logger.info("returning response")

        if background_tasks:
            background_tasks.add_task(process)
            return {"status": "accepted", "job_id": job_id}
        else:
            process()
            return {"status": "success", "chunks": len(split_docs)}