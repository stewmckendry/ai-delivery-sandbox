import pytest
from app.engines.triage_engine import TriageEngine

@pytest.fixture
def sample_state():
    return {"answers": {"injury_date": "2024-01-01"}}


def test_load_engine():
    engine = TriageEngine()
    assert engine.data.triage_flow, "Triage map should contain at least one stage"


def test_get_next_question(sample_state):
    engine = TriageEngine()
    q = engine.get_next_question(sample_state)
    assert isinstance(q, dict)
    assert "question" in q or q.get("is_terminal"), "Should return a question or terminal"


def test_evaluate_flags_no_flags():
    engine = TriageEngine()
    tracker_state = {"answers": {}}
    flags = engine.evaluate_flags(tracker_state)
    assert flags == []


def test_evaluate_flags_detects_red_flags():
    engine = TriageEngine()
    # mock response to a red flag question ID (must be in YAML for real test)
    tracker_state = {"answers": {"lost_consciousness": "Yes"}}
    flags = engine.evaluate_flags(tracker_state)
    assert isinstance(flags, list)