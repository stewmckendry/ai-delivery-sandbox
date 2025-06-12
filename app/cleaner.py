from __future__ import annotations

import hashlib
import re
from typing import Iterable, List, Dict, Callable, Union

from app.prompts import summarizer


# Tokenization is approximated by simple whitespace splitting.


def _sentences(text: str) -> List[str]:
    """Return a list of sentences in ``text`` using basic regex."""
    text = text.strip()
    if not text:
        return []
    return re.split(r"(?<=[.!?])\s+", text)


def _chunk_sentences(sentences: List[str], max_tokens: int) -> List[str]:
    """Combine sentences into chunks of approximately ``max_tokens`` words."""
    chunks: List[str] = []
    current: List[str] = []
    tokens = 0
    for sentence in sentences:
        sent_tokens = len(sentence.split())
        if current and tokens + sent_tokens > max_tokens:
            chunks.append(" ".join(current).strip())
            current = [sentence]
            tokens = sent_tokens
        else:
            current.append(sentence)
            tokens += sent_tokens
    if current:
        chunks.append(" ".join(current).strip())
    return chunks


def clean_blocks(
    blocks: Iterable[Union[str, Dict[str, str]]],
    *,
    max_chunk_tokens: int = 200,
    summary_token_threshold: int = 1000,
    summarize: Callable[[List[Dict]], str] = summarizer.summarize_blocks,
) -> List[str]:
    """Chunk, deduplicate, and optionally summarize text blocks.

    Parameters
    ----------
    blocks:
        Sequence of strings or dictionaries containing a ``text`` field.
    max_chunk_tokens:
        Maximum tokens per returned chunk before splitting.
    summary_token_threshold:
        If a chunk exceeds this many tokens it will be summarized using
        ``summarize``.
    summarize:
        Function accepting a list of dicts and returning a summary string. By
        default ``summarizer.summarize_blocks``.
    """

    segments: List[str] = []
    for block in blocks:
        text = block if isinstance(block, str) else block.get("text", "")
        for chunk in _chunk_sentences(_sentences(text), max_chunk_tokens):
            if len(chunk.split()) > summary_token_threshold:
                try:
                    chunk = summarize([{"text": chunk}])
                except Exception:
                    pass
            segments.append(chunk)

    deduped: List[str] = []
    seen = set()
    for seg in segments:
        h = hashlib.sha1(seg.encode("utf-8")).hexdigest()
        if h not in seen:
            seen.add(h)
            deduped.append(seg)

    return deduped
