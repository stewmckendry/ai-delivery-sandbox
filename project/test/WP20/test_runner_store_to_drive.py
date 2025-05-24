import os
from app.tools.tool_wrappers.storeToDrive import Tool

if __name__ == "__main__":
    test_input = {
        "final_markdown": "# Test Document\nThis is a test upload to Google Drive.",
        "artifact_id": "demo-artifact",
        "gate_id": "gate1",
        "version": "v0.1-test",
        "title": "Test Upload Document"
    }

    tool = Tool()
    try:
        result = tool.run_tool(test_input)
        print("✅ Upload successful! Drive URL:", result["drive_url"])
    except Exception as e:
        print("❌ Upload failed with error:", str(e))