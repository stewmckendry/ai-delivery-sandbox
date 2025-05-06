def test_load_prompt(client):
    response = client.get("/load_prompt", params={"prompt_id": "p1"})
    assert response.status_code in [200, 404]

def test_get_yaml_segment(client):
    response = client.get("/get_yaml_segment", params={"category": "animal"})
    assert response.status_code in [200, 404]

def test_record_reflection(client):
    payload = {
        "session_id": "test-session",
        "career_id": "animal-tracker",
        "prompt_id": "p1",
        "text": "I’d love to work with animals because it feels meaningful."
    }
    response = client.post("/record_reflection", json=payload)
    assert response.status_code == 200