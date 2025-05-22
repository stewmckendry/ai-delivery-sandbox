from fastapi import APIRouter, Request
from app.tools.tool_registry import ToolRegistry
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()
registry = ToolRegistry()

@router.get("/status")
def get_status():
    return {"status": "ok"}

@router.get("/tools")
def list_tools():
    return registry.list_tools()

@router.post("/tools/{tool_id}")
async def run_tool(tool_id: str, request: Request):
    logger.info(f"Running tool: {tool_id}")
    input_data = await request.json()
    logger.info(f"Input data: {input_data}")
    tool = registry.get_tool(tool_id)
    logger.info(f"Tool instance: {tool}")
    try:
        logger.info("Running tool with input data")
        return tool.run_tool(input_data)
    except ValueError as ve:
        logger.error(f"Validation error in tool {tool_id}: {ve}")
        return {"error": str(ve)}