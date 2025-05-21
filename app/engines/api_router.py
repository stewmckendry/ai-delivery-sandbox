from fastapi import APIRouter, Request, HTTPException
from app.tools.tool_registry import ToolRegistry

router = APIRouter()
registry = ToolRegistry()

@router.get("/status")
def status():
    return {"status": "ok"}

@router.post("/tools/{tool_id}")
def run_tool(tool_id: str, request: Request):
    tool = registry.get_tool(tool_id)
    if not tool:
        raise HTTPException(status_code=404, detail="Tool not found")

    input_dict = request.json()
    output = tool.run_tool(input_dict)
    return output