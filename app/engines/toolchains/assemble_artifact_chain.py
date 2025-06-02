import logging
import uuid
import re
from app.tools.tool_registry import ToolRegistry
from app.engines.memory_sync import log_tool_usage, save_document_and_trace, save_artifact_and_trace
from app.engines.project_profile_engine import ProjectProfileEngine
from app.redis.section_review_store import fetch_review_section

logger = logging.getLogger(__name__)

class AssembleArtifactChain:
    def __init__(self):
        registry = ToolRegistry()
        self.loader = registry.get_tool("loadSectionMetadata")
        self.formatter = registry.get_tool("formatSection")
        self.merger = registry.get_tool("mergeSections")
        self.finalizer = registry.get_tool("finalizeDocument")
        self.committer = registry.get_tool("storeToDrive")

    def run_tool(self, inputs):
        trace = []
        session_id = inputs.get("session_id")
        artifact_id = inputs.get("artifact_id")
        gate_id = inputs.get("gate_id")
        version = inputs.get("version", "v0.1")
        project_id = inputs.get("project_id")

        logger.info(f"Starting AssembleArtifactChain for artifact {artifact_id}, gate {gate_id}, session {session_id}, version {version}, project {project_id}")
        loaded = self.loader.run_tool(inputs)
        log_tool_usage("loadSectionMetadata", "loaded sections", loaded, session_id, None, inputs)
        trace.append({"tool": "loadSectionMetadata", "output": loaded})
        logger.info("[Step 1] loadSectionMetadata complete")
        logger.info(f"Loaded sections for artifact {artifact_id} with {len(loaded['ordered_sections'])} sections")

        #load project profile if available
        if project_id:
            profile_engine = ProjectProfileEngine()
            project_profile = profile_engine.load_profile(project_id)
            logger.info(f"Loaded project profile for project {project_id}: {project_profile}")
        else:
            project_profile = {}
            logger.warning(f"No project profile found for project_id {project_id}")
        inputs["project_profile"] = project_profile
        title = project_profile.get("title") or loaded.get("artifact_name", f"Assembled Artifact for {artifact_id}")
        logger.info(f"Using title: {title}")

        formatted_sections = []
        section_metadata = []
        for sec in loaded["ordered_sections"]:
            section_id = sec["section_id"]

            # Attempt to fetch from Redis first
            redis_fallback = False
            try:
                cached = fetch_review_section(project_id, artifact_id, session_id, sec["section_id"])
                if cached and cached.get("text"):
                    section_text = cached["text"]
                    logger.info(f"[Redis HIT] Using cached section for {sec['section_id']}")
                    log_tool_usage("fetchReviewSection", "fetched section from Redis", cached, session_id, None, inputs)
                else:
                    section_text = sec["text"]
                    redis_fallback = True
                    log_tool_usage("fetchReviewSection", "section not found in Redis", None, session_id, None, inputs)
            except Exception as e:
                section_text = sec["text"]
                redis_fallback = True
                logger.warning(f"[Redis ERROR] Failed to fetch {sec['section_id']}: {e}")
                log_tool_usage("fetchReviewSection", "error fetching section from Redis", None, session_id, e, inputs)

            if redis_fallback:
                logger.info(f"[Redis MISS] Falling back to DB for section {sec['section_id']}")

            formatted = self.formatter.run_tool({
                "section_id": section_id,
                "section_text": section_text,
                "section_title": sec["section_title"],
                "artifact_id": artifact_id
            })
            logger.info(f"Formatted section {section_id} with title '{sec['section_title']}'")
            log_tool_usage("formatSection", "formatted section", formatted, session_id, None, inputs)
            trace.append({"tool": "formatSection", "output": formatted})
            formatted_sections.append(formatted["formatted_section"])
            section_metadata.append({"section_id": sec["section_id"], "section_title": sec["section_title"]})
        logger.info("[Step 2] formatSection complete")
        logger.info(f"Formatted {len(formatted_sections)} sections for artifact {artifact_id}")

        merged = self.merger.run_tool({"sections": formatted_sections})
        log_tool_usage("mergeSections", "merged body", merged, session_id, None, inputs)
        trace.append({"tool": "mergeSections", "output": merged})
        logger.info("[Step 3] mergeSections complete")
        logger.info(f"Merged document body for artifact {artifact_id}.  Body snippet: {merged['document_body'][:100]}...")

        finalized = self.finalizer.run_tool({
            "title": title,
            "document_body": merged["document_body"],
            "artifact_id": artifact_id,
            "gate_id": str(gate_id),
            "version": version,
            "sections": [{"section_id": s["section_id"], "title": s["section_title"]} for s in section_metadata]
        })
        log_tool_usage("finalizeDocument", "finalized output", finalized, session_id, None, inputs)
        trace.append({"tool": "finalizeDocument", "output": finalized})
        logger.info("[Step 4] finalizeDocument complete")
        logger.info(f"Finalized document for artifact {artifact_id}.  Final markdown snippet: {finalized['final_markdown'][:100]}...")

        committed = self.committer.run_tool({
            "final_markdown": finalized["final_markdown"],
            "artifact_id": str(artifact_id),
            "gate_id": str(gate_id),
            "version": version,
            "title": title,
            "project_id": project_id
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

        return {
            "drive_url": committed.get("drive_url"),
            "message": (
                f"The artifact has been finalized and uploaded to Drive.\n\n"
                f"📄 [Download Link]({committed.get('drive_url')})\n\n"
                "Would you like to:\n"
                "1. Share feedback on the full draft? ➤ Call `submitFeedback`\n"
                "2. Start a new artifact? ➤ Re-run `getArtifactRequirements`"
            )
        }

