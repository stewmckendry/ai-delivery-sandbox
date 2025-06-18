import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.storage import files


def test_save_and_delete(tmp_path, monkeypatch):
    monkeypatch.setattr(files, "RAW_DIR", tmp_path)
    monkeypatch.setattr(files, "INDEX_FILE", tmp_path / "file_index.json")

    path = files.save_file("hi", "foo.txt", "test", {})
    assert path.exists()
    index = json.loads((tmp_path / "file_index.json").read_text())
    assert index and index[0]["filename"] == path.name

    files.delete_file(path)
    assert not path.exists()
    index = json.loads((tmp_path / "file_index.json").read_text())
    assert index == []
