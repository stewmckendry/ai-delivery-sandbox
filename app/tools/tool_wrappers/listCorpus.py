import logging
import os
from chromadb import HttpClient
from app.engines.memory_sync import log_tool_usage

logger = logging.getLogger(__name__)
logger.info("✅ listCorpus Tool loaded")

CHROMA_DIR = os.getenv("CHROMA_DIR", "./local_vector_store")
CHROMA_HOST = os.getenv("CHROMA_SERVER_HOST")
CHROMA_PORT = os.getenv("CHROMA_SERVER_HTTP_PORT", "8000")
USE_REMOTE_CHROMA = CHROMA_HOST is not None
logger.debug("USE_REMOTE_CHROMA: %s", USE_REMOTE_CHROMA)
logger.debug("CHROMA_HOST: %s", CHROMA_HOST)
logger.debug("CHROMA_PORT: %s", CHROMA_PORT)

class Tool:

    def run_tool(self, input_dict):
        logger.info("📋 Listing reference documents from Chroma corpus")

        if USE_REMOTE_CHROMA:
            client = HttpClient(host=CHROMA_HOST, port=int(CHROMA_PORT))
            collection = client.get_or_create_collection("policygpt")
            results = collection.get(include=["metadatas"], limit=100)

            seen = set()
            documents = []
            for meta in results.get("metadatas", []):
                title = meta.get("title", "Untitled")
                source = meta.get("source", "Unknown")
                date = meta.get("date", "n.d.")
                # Use a tuple of title and source as a unique identifier
                doc_id = (title, source)
                if doc_id not in seen:
                    seen.add(doc_id)
                    documents.append({
                        "title": title,
                        "source": source,
                        "date": date,
                        "url": meta.get("url", "")
                    })


            logger.info(f"📄 Retrieved {len(documents)} reference documents from remote Chroma")

            output = { "documents": documents }

            session_id = input_dict.get("session_id", "unknown_session")
            user_id = input_dict.get("user_id", "unknown_user")
            log_tool_usage("listCorpus", "reference_summary | listCorpus", output, session_id, user_id, input_dict)

            return output

        else:
            logger.warning("🚫 Local Chroma not supported for listCorpus tool")
            return { "documents": [] }
