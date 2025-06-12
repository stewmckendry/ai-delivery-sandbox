import openai

from app.extractor import extract_relevant_content


def test_extract_relevant_content(monkeypatch):
    calls = []

    def fake_create(*args, **kwargs):
        calls.append(kwargs["messages"][0]["content"])
        return {
            "choices": [
                {"message": {"content": '[{"type": "lab_result", "text": "Sodium 140 mmol/L"}]'}}
            ]
        }

    monkeypatch.setattr(openai.ChatCompletion, "create", fake_create)

    html = "<html><body><p>Sodium 140 mmol/L</p><p>Another value</p></body></html>"
    results = extract_relevant_content(html, "https://portal.test/page", max_chunk_chars=20)

    assert len(results) == len(calls)
    assert all(r["type"] == "lab_result" for r in results)
    assert results[0]["source_url"] == "https://portal.test/page"
    assert len(calls) > 1  # ensures chunking occurred
