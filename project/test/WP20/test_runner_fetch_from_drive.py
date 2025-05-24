import logging
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))

from app.tools.tool_wrappers.fetchFromDrive import Tool

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_fetch_test():
    input_data = {
        "gate_id": "0",
        "artifact_id": "investment_proposal_concept",
        "version": "v0.1"
    }
    try:
        result = Tool().run_tool(input_data)
        logger.info("✅ Fetch succeeded: %s", result)
    except Exception as e:
        logger.error("❌ Fetch failed: %s", str(e))

if __name__ == "__main__":
    run_fetch_test()