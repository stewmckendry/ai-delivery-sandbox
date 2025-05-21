import os
import sys
import argparse
from app.tools.tool_wrappers.text_extractor import extract_text
from app.tools.tool_wrappers.structured_input_ingestor import structure_input
from app.tools.tool_wrappers.retry_ingestion import retry_with_backoff
from app.tools.tool_wrappers.uploadTextInput import Tool as UploadTextTool

SAVE_DIR = "project/logs/ingest_traces"
os.makedirs(SAVE_DIR, exist_ok=True)

def ingest_file(file_path, input_type):
    raw = retry_with_backoff(extract_text, file_path=file_path)
    if raw is None:
        return
    entry = structure_input(raw, file_path, input_type)
    tool = UploadTextTool()
    result = tool.run_tool(entry)
    print("DB ingest result:", result)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("inputs", nargs='+', help="Paths to input files")
    parser.add_argument("--type", default="uploadFileInput", help="Type of input")
    args = parser.parse_args()

    for file_path in args.inputs:
        ingest_file(file_path, args.type)

if __name__ == "__main__":
    main()