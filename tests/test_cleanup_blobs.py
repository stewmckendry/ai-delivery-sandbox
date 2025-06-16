import importlib
import sys
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def test_cleanup_blobs(monkeypatch, capsys):
    module = importlib.import_module("scripts.cleanup_blobs")

    now = datetime.utcnow()
    blobs = [
        {"name": "user/old.txt", "last_modified": now - timedelta(hours=25), "age_hours": 25},
        {"name": "user/new.txt", "last_modified": now - timedelta(minutes=30), "age_hours": 0.5},
    ]

    monkeypatch.setattr(module.blob, "list_blob_info", lambda prefix: blobs)
    deleted = []
    monkeypatch.setattr(module.blob, "delete_blob", lambda name: deleted.append(name))
    monkeypatch.setattr(sys, "argv", ["cleanup_blobs.py", "--prefix", "user", "--ttl-hours", "1"])

    module.main()
    output = capsys.readouterr().out
    assert "1 expired blobs" in output
    assert deleted == ["user/old.txt"]
