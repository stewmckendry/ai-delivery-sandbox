import openai
import types
from app.prompts.summarizer import summarize_lab_results


def test_summarize_lab_results(monkeypatch):
    # Prepare fake response
    def fake_create(*args, **kwargs):
        return {"choices": [{"message": {"content": "Summary text"}}]}

    monkeypatch.setattr(openai.ChatCompletion, "create", fake_create)

    labs = [
        {"test_name": "Cholesterol", "value": 5.8, "units": "mmol/L", "date": "2023-05-01"},
        {"test_name": "Hemoglobin", "value": 13.5, "units": "g/dL", "date": "2023-05-02"},
    ]

    summary = summarize_lab_results(labs)
    assert summary == "Summary text"
