from __future__ import annotations

import os
from typing import Iterable, List

import chromadb
from chromadb.api import ClientAPI
from chromadb.api.types import Documents, Embeddings, IDs, Metadatas
from chromadb.config import Settings
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction


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


_embed = OpenAIEmbeddingFunction()


def _chunk(text: str, size: int = 500) -> List[str]:
    return [text[i : i + size] for i in range(0, len(text), size)]


def index_structured_records(records: Iterable, session_key: str) -> None:
    """Index structured record objects for a session."""
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
            metas.append(
                {
                    "session_key": session_key,
                    "type": getattr(rec, "clinical_type", None) or getattr(rec, "type", None),
                    "code": getattr(rec, "code", None),
                    "date": str(getattr(rec, "date", "")),
                }
            )

    if docs:
        collection.add(documents=docs, ids=ids, metadatas=metas)
