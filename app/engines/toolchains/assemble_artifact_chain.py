import logging
import uuid
from app.tools.tool_registry import ToolRegistry
from app.engines.memory_sync import log_tool_usage, save_document_and_trace

logger = logging.getLogger(__name__)

class AssembleArtifactChain:
    def __init__(self):
        registry = ToolRegistry()
        self.loader = registry.get_tool("loadSectionMetadata")
        self.formatter = registry.get_tool("formatSection")
        self.merger = registry.get_tool("mergeSections")
        self.finalizer = registry.get_tool("finalizeDocument")
        self.committer = registry.get_tool("storeToDrive")  # Replaces commitArtifact

    def run(self, inputs):
        trace = []
        session_id = str(uuid.uuid4())
        artifact_id = inputs["artifact_id"]
        gate_id = inputs["gate_id"]
        version = inputs.get("version", "v0.1")

        # Step 1: Load
        loaded = self.loader.run_tool({"artifact_id": str(artifact_id), "gate_id": str(gate_id)})
        log_tool_usage("loadSectionMetadata", "loaded sections", loaded, session_id, None, inputs)
        trace.append({"tool": "loadSectionMetadata", "output": loaded})
        logger.info("[Step 1] loadSectionMetadata complete")

        title = loaded.get("artifact_name", f"Assembled Artifact for {artifact_id}")

        # Step 2: Format
        formatted_sections = []
        for sec in loaded["ordered_sections"]:
            formatted = self.formatter.run_tool({
                "section_id": sec["section_id"],
                "section_text": sec["text"],
                "section_title": sec["section_title"],
                "artifact_id": artifact_id
            })
            log_tool_usage("formatSection", "formatted section", formatted, session_id, None, inputs)
            trace.append({"tool": "formatSection", "output": formatted})
            formatted_sections.append(formatted["formatted_section"])
        logger.info("[Step 2] formatSection complete")

        # Step 3: Merge
        merged = self.merger.run_tool({"sections": formatted_sections})
        log_tool_usage("mergeSections", "merged body", merged, session_id, None, inputs)
        trace.append({"tool": "mergeSections", "output": merged})
        logger.info("[Step 3] mergeSections complete")

        # Step 4: Finalize
        finalized = self.finalizer.run_tool({
            "title": title,
            "document_body": merged["document_body"],
            "artifact_id": artifact_id,
            "gate_id": gate_id,
            "version": version
        })
        log_tool_usage("finalizeDocument", "finalized output", finalized, session_id, None, inputs)
        trace.append({"tool": "finalizeDocument", "output": finalized})
        logger.info("[Step 4] finalizeDocument complete")

        # Step 5: Commit to Drive
        committed = self.committer.run_tool({
            "final_markdown": finalized["final_markdown"],
            "artifact_id": artifact_id,
            "gate_id": gate_id,
            "version": version,
            "title": title
        })
        log_tool_usage("storeToDrive", "committed", committed, session_id, None, inputs)
        trace.append({"tool": "storeToDrive", "output": committed})
        logger.info("[Step 5] storeToDrive complete")

        # Save logs
        save_document_and_trace(
            session_id=session_id,
            artifact_id=artifact_id,
            gate_id=gate_id,
            version=version,
            storage_url=committed.get("drive_url"),
            summary=f"Assembled artifact {artifact_id} gate {gate_id}",
            inputs=inputs,
            output_path=None,
            tool_outputs=trace
        )
        logger.info("[Step 6] Saved to Artifact and ReasoningTrace")

        return {"final_output": committed, "trace": trace}