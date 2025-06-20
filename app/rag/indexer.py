from __future__ import annotations

import os
import logging
from typing import Iterable, List

import chromadb
from chromadb.api import ClientAPI
from chromadb.api.types import Documents, Embeddings, IDs, Metadatas
from chromadb.config import Settings
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction

from dotenv import load_dotenv
load_dotenv()

logger = logging.getLogger(__name__)

_COLLECTION = "health_records"


def _get_client() -> ClientAPI:
    """Return a Chroma client based on environment settings."""
    if os.getenv("USE_REMOTE_CHROMA", "false").lower() == "true":
        host = os.getenv("CHROMA_SERVER_HOST", "localhost")
        port = int(os.getenv("CHROMA_SERVER_HTTP_PORT", "8000"))
        token = os.getenv("CHROMA_TOKEN")
        headers = {"Authorization": f"Bearer {token}"} if token else None
        return chromadb.HttpClient(host=host, port=port, headers=headers)
    return chromadb.Client(Settings(allow_reset=True))


_embed = OpenAIEmbeddingFunction(api_key=os.getenv("OPENAI_API_KEY"))


def _chunk(text: str, size: int = 500) -> List[str]:
    return [text[i : i + size] for i in range(0, len(text), size)]


def index_structured_records(records: Iterable, session_key: str) -> None:
    """Index structured record objects for a session."""
    records = list(records)
    client = _get_client()
    collection = client.get_or_create_collection(_COLLECTION, embedding_function=_embed)

    ids: List[str] = []
    docs: Documents = []
    metas: Metadatas = []

    for rec in records:
        text = getattr(rec, "text", "")
        for i, chunk in enumerate(_chunk(text)):
            ids.append(f"{session_key}_{rec.id}_{i}")
            docs.append(chunk)
            meta = {
                "session_key": session_key,
                "type": getattr(rec, "clinical_type", None)
                or getattr(rec, "type", None)
                or "",
                "code": getattr(rec, "code", None) or "",
                "display": getattr(rec, "display", None) or "",
                "source_url": getattr(rec, "source_url", None) or "",
                "portal": getattr(rec, "portal", None) or "",
                "date": str(getattr(rec, "date", "")),
            }
            metas.append({k: v for k, v in meta.items() if v is not None})

    if docs:
        collection.add(documents=docs, ids=ids, metadatas=metas)
        logger.info(
            "[rag.indexer] added %d records (%d chunks) for session %s",
            len(records),
            len(docs),
            session_key,
        )
    else:
        logger.error("[rag.indexer] no records to index for session %s", session_key)
