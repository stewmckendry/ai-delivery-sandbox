# filename: cli_create_snapshot.py

from app.tools.tool_wrappers.createSessionSnapshot import Tool
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--session_id", required=False, help="Optional session ID for filtering")
    args = parser.parse_args()

    tool = Tool()
    output = tool.run_tool({"session_id": args.session_id})
    print(output)
