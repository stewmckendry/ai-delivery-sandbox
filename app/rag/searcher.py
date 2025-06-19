from __future__ import annotations

import os
from typing import List, Dict

import chromadb
from chromadb.api import ClientAPI
from chromadb.config import Settings
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction

from dotenv import load_dotenv
load_dotenv()

_COLLECTION = "health_records"


def _get_client() -> ClientAPI:
    if os.getenv("USE_REMOTE_CHROMA", "false").lower() == "true":
        host = os.getenv("CHROMA_SERVER_HOST", "localhost")
        port = int(os.getenv("CHROMA_SERVER_HTTP_PORT", "8000"))
        token = os.getenv("CHROMA_TOKEN")
        headers = {"Authorization": f"Bearer {token}"} if token else None
        return chromadb.HttpClient(host=host, port=port, headers=headers)
    return chromadb.Client(Settings(allow_reset=True))


_embed = OpenAIEmbeddingFunction(api_key=os.getenv("OPENAI_API_KEY"))


def search_records(query: str, session_key: str, n_results: int = 5) -> List[Dict]:
    """Return top matching records for ``query`` within a session."""
    client = _get_client()
    collection = client.get_or_create_collection(_COLLECTION, embedding_function=_embed)

    results = collection.query(
        query_texts=[query],
        n_results=n_results,
        where={"session_key": session_key},
    )

    docs = results.get("documents", [[]])[0]
    metas = results.get("metadatas", [[]])[0]

    records: List[Dict] = []
    for doc, meta in zip(docs, metas):
        record = {"text": doc}
        if isinstance(meta, dict):
            record.update(meta)
        records.append(record)
    return records
