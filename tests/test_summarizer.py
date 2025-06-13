from app.prompts.summarizer import summarize_blocks
from app.utils import llm


def test_summarize_blocks(monkeypatch):
    # Prepare fake response
    def fake_create(messages, **_kwargs):
        return "Summary text"

    monkeypatch.setattr(llm, "chat_completion", fake_create)
    import app.prompts.summarizer as summarizer_module
    monkeypatch.setattr(summarizer_module, "chat_completion", fake_create)

    blocks = [
        {"text": "Patient reports mild headache."},
        {"text": "Blood pressure within normal range."},
    ]

    summary = summarize_blocks(blocks)
    assert summary == "Summary text"
