import requests
import yaml

def load_yaml_from_github(url):
    resp = requests.get(url)
    resp.raise_for_status()
    return yaml.safe_load(resp.text)

def load_triage_map():
    url = "https://raw.githubusercontent.com/stewmckendry/ai-delivery-sandbox/sandbox-silver-tiger/reference/triage_map.yaml"
    return load_yaml_from_github(url)

def load_stages_yaml():
    url = "https://raw.githubusercontent.com/stewmckendry/ai-delivery-sandbox/sandbox-silver-tiger/reference/stages.yaml"
    return load_yaml_from_github(url)