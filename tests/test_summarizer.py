import openai
from app.prompts.summarizer import summarize_blocks


def test_summarize_blocks(monkeypatch):
    # Prepare fake response
    def fake_create(*args, **kwargs):
        return {"choices": [{"message": {"content": "Summary text"}}]}

    monkeypatch.setattr(openai.ChatCompletion, "create", fake_create)

    blocks = [
        {"text": "Patient reports mild headache."},
        {"text": "Blood pressure within normal range."},
    ]

    summary = summarize_blocks(blocks)
    assert summary == "Summary text"
