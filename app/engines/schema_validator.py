import argparse
import yaml
from pathlib import Path
from pydantic import ValidationError
from app.models.triage import TriageMap
from app.models.stage import StageMap

# Mapping schema names to model classes and default file paths
SCHEMA_MODELS = {
    "triage": (TriageMap, "reference/triage_map.yaml"),
    "stage": (StageMap, "reference/stages.yaml")
}

def validate_file(schema_name: str, file_path: str):
    """
    Validate a given YAML file against a registered pydantic schema.
    """
    model_cls, _ = SCHEMA_MODELS[schema_name]
    print(f"Validating {file_path} as {schema_name} schema...")
    with open(file_path) as f:
        try:
            raw = yaml.safe_load(f)
            model_cls(**raw)
            print("✅ Validation passed.")
        except ValidationError as e:
            print("❌ Validation failed:")
            print(e.json())
            exit(1)
        except Exception as e:
            print(f"❌ Error reading file: {e}")
            exit(1)

def validate_all():
    """
    Validate all known YAMLs using predefined schema map.
    """
    for schema_name, (_, path) in SCHEMA_MODELS.items():
        validate_file(schema_name, path)

if __name__ == "__main__":
    # CLI to run validation interactively or in CI
    parser = argparse.ArgumentParser()
    parser.add_argument("--schema", choices=SCHEMA_MODELS.keys())  # target schema
    parser.add_argument("--file")  # target file path
    parser.add_argument("--all", action="store_true")  # flag to run all checks
    args = parser.parse_args()

    if args.all:
        validate_all()
    elif args.schema and args.file:
        validate_file(args.schema, args.file)
    else:
        print("❌ Must provide either --all or both --schema and --file")
        exit(1)