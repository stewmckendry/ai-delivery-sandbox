from __future__ import annotations

import json
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, Union

# Directory to store raw files
RAW_DIR = Path("data/raw")
INDEX_FILE = RAW_DIR / "file_index.json"

def save_file(content: Union[str, bytes], filename: str, portal_name: str, metadata: Dict[str, Any]) -> Path:
    """Save raw ``content`` to ``RAW_DIR`` and update index.

    Parameters
    ----------
    content: str | bytes
        File content to write. String content is encoded as UTF-8.
    filename: str
        Original file name (used for extension).
    portal_name: str
        Name of the portal where the content came from.
    metadata: dict[str, Any]
        Additional metadata to store alongside the file.

    Returns
    -------
    Path
        Location of the saved file.
    """

    RAW_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    ext = Path(filename).suffix or ""
    target_name = f"{portal_name}_{timestamp}{ext}"
    target_path = RAW_DIR / target_name

    if isinstance(content, str):
        data = content.encode("utf-8")
    else:
        data = content

    with target_path.open("wb") as f:
        f.write(data)

    # Load existing index
    if INDEX_FILE.exists():
        with INDEX_FILE.open("r", encoding="utf-8") as f:
            index = json.load(f)
    else:
        index = []

    # Append new record
    record = {
        "filename": target_name,
        "portal": portal_name,
        "timestamp": timestamp,
        "metadata": metadata,
    }
    index.append(record)

    with INDEX_FILE.open("w", encoding="utf-8") as f:
        json.dump(index, f, indent=2)

    return target_path
