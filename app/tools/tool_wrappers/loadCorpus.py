import logging
import os
import uuid
import json
from datetime import datetime
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
import requests
import requests
from bs4 import BeautifulSoup
from app.tools.utils.llm_helpers import get_prompt, chat_completion_request
from jinja2 import Template

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

CHROMA_DIR = os.getenv("CHROMA_DIR", "./local_vector_store")
CHROMA_HOST = os.getenv("CHROMA_SERVER_HOST")
CHROMA_PORT = os.getenv("CHROMA_SERVER_HTTP_PORT", "8000")
USE_REMOTE_CHROMA = True
logger.info("USE_REMOTE_CHROMA: %s", USE_REMOTE_CHROMA)
logger.info("CHROMA_HOST: %s", CHROMA_HOST)
logger.info("CHROMA_PORT: %s", CHROMA_PORT)

class Tool:
    async_tool = True  # Enables async execution in api_router

    def run_tool(self, input_dict, background_tasks: BackgroundTasks = None):
        logger.info("Running loadCorpus tool")

        job_id = str(uuid.uuid4())

        def process():
            logger.info("🚀 Starting async loadCorpus tool")

            file_contents = input_dict.get("file_contents")
            file_url = input_dict.get("file_url")
            if not file_contents and file_url:
                try:
                    response = requests.get(file_url)
                    response.raise_for_status()
                    soup = BeautifulSoup(response.text, "html.parser")
                    raw_text = soup.get_text(separator="\n", strip=True)
                    prompt_templates = get_prompt("search_prompts.yaml", "search_cleanup")
                    system_prompt = Template(prompt_templates["system"]).render()
                    user_prompt = Template(prompt_templates["user"]).render(raw_text=raw_text, file_url=file_url)
                    logger.info(f"[Tool] loadCorpus user prompt: {user_prompt[:100]}...")
                    cleaned = chat_completion_request(system_prompt, user_prompt, temperature=0.4)
                    file_contents = cleaned.strip()
                    log_tool_usage(
                        "loadCorpus",
                        f"Fetched and cleaned content from {file_url}.  User prompt: {user_prompt[:100]}...",
                        json.dumps({"status": "success", "length": len(file_contents)}, indent=2),
                        session_id=input_dict.get("session_id"),
                        user_id=input_dict.get("user_id"),
                        metadata=input_dict.get("metadata", {})
                    )
                except Exception as e:
                    logger.error(f"Failed to fetch file from URL: {file_url}", exc_info=e)
                    raise ValueError(f"Error fetching file from {file_url}: {e}")

            file_name = input_dict.get("file_name", "Unnamed Document")
            metadata = input_dict.get("metadata", {})

            metadata.setdefault("title", file_name)
            metadata.setdefault("source", "Internal Knowledge Base")
            metadata.setdefault("date", datetime.utcnow().date().isoformat())

            text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
            document = Document(page_content=file_contents)
            split_docs = text_splitter.split_documents([document])
            for doc in split_docs:
                doc.metadata.update(metadata)

            if USE_REMOTE_CHROMA:
                logger.info("Using remote Chroma server for indexing")
                client = HttpClient(host=CHROMA_HOST, port=int(CHROMA_PORT))
                collection = client.get_or_create_collection("policygpt")
                for doc in split_docs:
                    doc_id = str(uuid.uuid4())
                    doc.metadata["doc_id"] = doc_id
                    collection.add(documents=[doc.page_content], metadatas=[doc.metadata], ids=[doc_id])
            else:
                logger.info("Using local Chroma vector store for indexing")
                vectorstore = Chroma.from_documents(split_docs, OpenAIEmbeddings(), persist_directory=CHROMA_DIR)
                vectorstore.persist()

            entry = structure_input(file_contents, file_name, tool_name="loadCorpus", metadata=metadata)
            out_path = write_trace(entry)
            log_tool_usage(
                entry["tool"],
                entry["input_summary"],
                json.dumps({"status": "success", "chunks": len(split_docs)}, indent=2),
                session_id=entry.get("session_id"),
                user_id=entry.get("user_id"),
                metadata=entry.get("metadata")
            )
            logger.info("🚀 loadCorpus tool completed successfully")

        if background_tasks:
            background_tasks.add_task(process)
            logger.info("🚀 Job %s accepted for background processing", job_id)
            return {
                "status": "accepted",
                "job_id": job_id,
                "instructions": "Document accepted for background processing and will be indexed shortly. Next steps: you can upload more reference materials, record research notes using `record_research`, upload project-specific inputs using `ingestInputChain`, or begin drafting a section using `generate_section_chain`."
            }
        else:
            process()
            logger.info("🚀 Job %s processed synchronously", job_id)
            return {
                "status": "success",
                "chunks": len(split_docs),
                "instructions": "Document uploaded and successfully indexed. Next steps: you can upload more reference materials, record research notes using `record_research`, upload project-specific inputs using `ingestInputChain`, or begin drafting a section using `generate_section_chain`."
            }
