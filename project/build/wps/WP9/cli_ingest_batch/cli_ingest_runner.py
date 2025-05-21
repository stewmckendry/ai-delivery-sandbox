import os
import sys
import argparse
from text_extractor import extract_text
from structured_input_ingestor import structure_input, to_yaml
from retry_ingestion import retry_with_backoff

SAVE_DIR = "project/logs/ingest_traces"
os.makedirs(SAVE_DIR, exist_ok=True)

def ingest_file(file_path, input_type):
    raw = retry_with_backoff(extract_text, file_path=file_path)
    if raw is None:
        return
    entry = structure_input(raw, file_path, input_type)
    yaml_out = to_yaml(entry)
    out_path = os.path.join(SAVE_DIR, os.path.basename(file_path) + ".yaml")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(yaml_out)
    print(f"Ingested and saved to {out_path}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("inputs", nargs='+', help="Paths to input files")
    parser.add_argument("--type", default="uploadFileInput", help="Type of input")
    args = parser.parse_args()
    
    for file_path in args.inputs:
        ingest_file(file_path, args.type)

if __name__ == "__main__":
    main()