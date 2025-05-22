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
    print(f"Running tool: {tool_id}")
    input_data = await request.json()
    print(f"Input data: {input_data}")
    tool = registry.get_tool(tool_id)
    print(f"Tool instance: {tool}")
    try:
        print("Running tool with input data")
        return tool.run_tool(input_data)
    except ValueError as ve:
        print(f"Validation error in tool {tool_id}: {ve}")
        return {"error": str(ve)}