import importlib
import logging


def test_classify_clinical_type_strips_wrappers(monkeypatch, caplog):
    import app.orchestrator as orch_module

    importlib.reload(orch_module)

    def fake_chat(_messages):
        return '```json\n{"clinical_type": "Procedure"}\n```'

    monkeypatch.setattr(orch_module, "chat_completion", fake_chat)
    caplog.set_level(logging.INFO)
    result = orch_module._classify_clinical_type("Check for infection")
    assert result[0] == "Procedure"
    assert "LLM clinical classification failed" not in caplog.text


def test_classify_clinical_type_invalid_json_falls_back(monkeypatch, caplog):
    import app.orchestrator as orch_module

    importlib.reload(orch_module)

    def fake_chat(_messages):
        return "{'clinical_type': 'Condition',}"

    monkeypatch.setattr(orch_module, "chat_completion", fake_chat)
    caplog.set_level(logging.WARNING)
    result = orch_module._classify_clinical_type("Patient has diabetes")
    assert result[0] == "Condition"
    assert "LLM clinical classification failed" in caplog.text
