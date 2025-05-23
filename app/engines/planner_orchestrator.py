import logging
from typing import Dict, Any

from app.engines.memory_sync import log_tool_usage, save_session_snapshot
from app.db.models import PromptLog, SessionSnapshot
from app.tools import TOOL_CATALOG

logger = logging.getLogger(__name__)

class PlannerOrchestrator:
    def __init__(self, mode: str = "live"):
        self.mode = mode  # 'live' or 'replay'
        self.trace = []

    def run(self, intent: str, inputs: Dict[str, Any]) -> Dict[str, Any]:
        logger.info(f"Planner starting for intent: {intent}")

        tool_chain = self.select_tool_chain(intent)
        session_state = {}

        for step, tool_name in enumerate(tool_chain):
            tool = TOOL_CATALOG.get(tool_name)
            if not tool:
                raise ValueError(f"Tool '{tool_name}' not found")

            tool_input = self.prepare_input(tool_name, inputs, session_state)
            if self.mode == "live":
                output = tool.run_tool(tool_input)
            else:
                output = self.load_from_log(tool_name, step)

            self.trace.append({
                "step": step,
                "tool": tool_name,
                "input": tool_input,
                "output": output
            })

            session_state[tool_name] = output

            if self.mode == "live":
                log_tool_usage(tool_name, tool_input, output)

        if self.mode == "live":
            save_session_snapshot(session_state)

        return {"final_output": output, "trace": self.trace}

    def select_tool_chain(self, intent: str):
        if intent == "generate_section":
            return ["memory_retrieve", "section_synthesizer", "section_refiner"]
        raise ValueError(f"No toolchain defined for intent: {intent}")

    def prepare_input(self, tool_name: str, inputs: Dict[str, Any], state: Dict[str, Any]):
        return inputs

    def load_from_log(self, tool_name: str, step: int):
        return f"[REPLAYED_OUTPUT for {tool_name} at step {step}]"