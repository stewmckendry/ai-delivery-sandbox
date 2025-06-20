import importlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def test_delete_blobs_names(monkeypatch, capsys):
    module = importlib.import_module("scripts.delete_blobs")

    deleted = []
    monkeypatch.setattr(module.blob, "delete_blob", lambda name: deleted.append(name))
    monkeypatch.setattr(module.blob, "list_blobs", lambda prefix: ["a", "b"])  # not used

    monkeypatch.setattr(sys, "argv", ["delete_blobs.py", "--name", "s1/file1", "--name", "s2/file2"])
    module.main()
    out = capsys.readouterr().out
    assert "Deleted 2 blobs" in out
    assert deleted == ["s1/file1", "s2/file2"]


def test_delete_blobs_all(monkeypatch, capsys):
    module = importlib.import_module("scripts.delete_blobs")

    monkeypatch.setattr(module.blob, "list_blobs", lambda prefix: ["x", "y", "z"])
    deleted = []
    monkeypatch.setattr(module.blob, "delete_blob", lambda name: deleted.append(name))

    monkeypatch.setattr(sys, "argv", ["delete_blobs.py", "--all"])
    module.main()
    out = capsys.readouterr().out
    assert "Deleted 3 blobs" in out
    assert deleted == ["x", "y", "z"]
