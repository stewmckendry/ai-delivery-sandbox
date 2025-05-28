import logging
import uuid
import re
from app.tools.tool_registry import ToolRegistry
from app.engines.memory_sync import log_tool_usage, save_document_and_trace, save_artifact_and_trace

logger = logging.getLogger(__name__)

class AssembleArtifactChain:
    def __init__(self):
        registry = ToolRegistry()
        self.loader = registry.get_tool("loadSectionMetadata")
        self.formatter = registry.get_tool("formatSection")
        self.merger = registry.get_tool("mergeSections")
        self.finalizer = registry.get_tool("finalizeDocument")
        self.committer = registry.get_tool("storeToDrive")
        self.refiner = registry.get_tool("refine_document_chain")

    def run(self, inputs):
        trace = []
        session_id = str(uuid.uuid4())
        artifact_id = inputs.get("artifact_id")
        gate_id = inputs.get("gate_id")
        version = inputs.get("version", "v0.1")

        loaded = self.loader.run_tool({"artifact_id": str(artifact_id), "gate_id": str(gate_id)})
        log_tool_usage("loadSectionMetadata", "loaded sections", loaded, session_id, None, inputs)
        trace.append({"tool": "loadSectionMetadata", "output": loaded})
        logger.info("[Step 1] loadSectionMetadata complete")

        profile = inputs.get("project_profile", {})
        title = profile.get("title") or loaded.get("artifact_name", f"Assembled Artifact for {artifact_id}")

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

        merged = self.merger.run_tool({"sections": formatted_sections})
        log_tool_usage("mergeSections", "merged body", merged, session_id, None, inputs)
        trace.append({"tool": "mergeSections", "output": merged})
        logger.info("[Step 3] mergeSections complete")

        refined = self.refiner.run_tool({"document_body": merged["document_body"], "title": title, "project_id": profile.get("project_id") or inputs.get("project_id")})
        log_tool_usage("refineDocumentChain", "refined body", refined, session_id, None, inputs)
        trace.append({"tool": "refineDocumentChain", "output": refined})
        logger.info("[Step 3.5] refineDocumentChain complete")

        # Save parsed refined body into ArtifactSection
        refined_text = refined["refined_body"]
        section_map = {s["section_title"].strip(): s["section_id"] for s in loaded["ordered_sections"]}
        parts = re.split(r"^##\s+(.+)$", refined_text, flags=re.MULTILINE)
        for i in range(1, len(parts), 2):
            title = parts[i].strip()
            body = parts[i + 1].strip()
            section_id = section_map.get(title)
            if section_id:
                save_artifact_and_trace(
                    session_id=session_id,
                    artifact_id=artifact_id,
                    gate_id=gate_id,
                    section_id=section_id,
                    text=body,
                    sources=[],
                    generated_by="refine_document",
                    project_id=profile.get("project_id")
                )
        logger.info("[Step 3.75] Updated ArtifactSection with refined content")

        finalized = self.finalizer.run_tool({
            "title": title,
            "document_body": refined["refined_body"],
            "artifact_id": artifact_id,
            "gate_id": gate_id,
            "version": version
        })
        log_tool_usage("finalizeDocument", "finalized output", finalized, session_id, None, inputs)
        trace.append({"tool": "finalizeDocument", "output": finalized})
        logger.info("[Step 4] finalizeDocument complete")

        committed = self.committer.run_tool({
            "final_markdown": finalized["final_markdown"],
            "artifact_id": artifact_id,
            "gate_id": gate_id,
            "version": version,
            "title": title,
            "project_id": profile.get("project_id")
        })
        log_tool_usage("storeToDrive", "committed", committed, session_id, None, inputs)
        trace.append({"tool": "storeToDrive", "output": committed})
        logger.info("[Step 5] storeToDrive complete")

        save_document_and_trace(
            session_id=session_id,
            artifact_id=artifact_id,
            gate_id=gate_id,
            version=version,
            storage_url=committed.get("drive_url"),
            summary=f"Assembled artifact {artifact_id} gate {gate_id}",
            inputs=inputs,
            output_path=committed.get("drive_url"),
            tool_outputs=trace
        )
        logger.info("[Step 6] Saved to Artifact and ReasoningTrace")

        return {"final_output": committed, "trace": trace}