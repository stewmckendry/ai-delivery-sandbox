from app.cleaner import clean_blocks


def test_clean_blocks_deduplication():
    blocks = [
        "A. B.",
        "B. C.",
    ]
    result = clean_blocks(blocks, max_chunk_tokens=1)
    assert result == ["A.", "B.", "C."]


def test_clean_blocks_summarization(monkeypatch):
    called = {"count": 0}

    def fake_sum(data):
        called["count"] += 1
        return "summary"

    text = " ".join(["word"] * 12)
    result = clean_blocks(
        [text],
        max_chunk_tokens=50,
        summary_token_threshold=10,
        summarize=fake_sum,
    )
    assert result == ["summary"]
    assert called["count"] == 1
