import argparse, yaml
from pathlib import Path

class Tool:
    def run_tool(self, input_dict):
        # Placeholder logic
        return {"status": "success", "step": "searchKnowledgeBase", "input_received": input_dict}

def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, required=True)
    args = parser.parse_args()

    input_path = Path(args.input)
    input_dict = yaml.safe_load(input_path.read_text())
    tool = Tool()
    output = tool.run_tool(input_dict)

    print("--- input")
    print(yaml.dump(input_dict))
    print("--- output")
    print(yaml.dump(output))

if __name__ == "__main__":
    cli()