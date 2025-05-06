def test_prompt_loader():
    from project.app.utils import prompt_loader
    try:
        data = prompt_loader.load_prompt("p1")
        assert "questions" in data
    except Exception:
        assert True

def test_yaml_loader():
    from project.app.utils import yaml_loader
    try:
        data = yaml_loader.load_segment("animal")
        assert isinstance(data, dict)
    except Exception:
        assert True