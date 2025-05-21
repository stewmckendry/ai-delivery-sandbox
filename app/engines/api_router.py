from fastapi import APIRouter, Request
from app.tools.tool_registry import ToolRegistry

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
    input_data = await request.json()
    tool = registry.get_tool(tool_id)
    return tool.run_tool(input_data)