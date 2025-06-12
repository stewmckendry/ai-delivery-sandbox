from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

# Location for audit log file can be overridden via AUDIT_LOG env var
AUDIT_PATH = Path(os.getenv("AUDIT_LOG", "data/audit_log.json"))


def log_event(user: str, action: str, context: Dict[str, Any]) -> None:
    """Append an audit record to ``AUDIT_PATH``.

    Each entry contains ``timestamp``, ``user``, ``action``, and ``context``.
    ``context`` should be JSON-serialisable.
    """
    AUDIT_PATH.parent.mkdir(parents=True, exist_ok=True)

    if AUDIT_PATH.exists():
        with AUDIT_PATH.open("r", encoding="utf-8") as f:
            entries = json.load(f)
    else:
        entries = []

    entries.append(
        {
            "timestamp": datetime.utcnow().isoformat(),
            "user": user,
            "action": action,
            "context": context,
        }
    )

    with AUDIT_PATH.open("w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2)
