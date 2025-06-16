import importlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def test_upload_to_blob(monkeypatch, tmp_path, capsys):
    module = importlib.import_module("scripts.upload_to_blob")

    file_path = tmp_path / "sample.txt"
    file_path.write_text("hello")

    generated = {}
    monkeypatch.setattr(
        module.blob,
        "generate_upload_url",
        lambda sess, filename: generated.setdefault("url", f"https://x/{sess}/{filename}")
    )

    put_called = {}

    class Resp:
        status_code = 201

        def raise_for_status(self):
            pass

    def fake_put(url, data):
        put_called["url"] = url
        put_called["data"] = data
        return Resp()

    monkeypatch.setattr(module.httpx, "put", fake_put)

    logged = {}
    def fake_record(session, portal, filename):
        logged.update({"session": session, "portal": portal, "filename": filename})
    monkeypatch.setattr(module.blob, "record_upload", fake_record)

    monkeypatch.setattr(
        sys,
        "argv",
        ["upload_to_blob.py", "--session-key", "sess", "--file", str(file_path), "--portal", "port"]
    )

    module.main()
    out = capsys.readouterr().out
    assert "Uploaded" in out
    assert generated["url"] == "https://x/sess/sample.txt"
    assert put_called["url"] == generated["url"]
    assert put_called["data"] == b"hello"
    assert logged == {"session": "sess", "portal": "port", "filename": "sample.txt"}
