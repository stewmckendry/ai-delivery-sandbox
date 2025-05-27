import logging
from app.tools.tool_registry import ToolRegistry
from app.engines.memory_sync import save_artifact_and_trace, log_tool_usage, save_feedback
from app.db.database import get_session
from app.db.models.ArtifactSection import ArtifactSection
from app.tools.llm.gpt import chat_completion_request

logger = logging.getLogger(__name__)

class ReviseSectionChain:
    def __init__(self):
        registry = ToolRegistry()
        self.memory_tool = registry.get_tool("memory_retrieve")
        self.feedback_preprocessor = registry.get_tool("feedback_preprocessor")
        self.feedback_mapper = registry.get_tool("feedback_mapper")
        self.section_rewriter = registry.get_tool("section_rewriter")
        self.manual_edit_tool = registry.get_tool("manualEditSync")

    def summarize_text(self, text):
        if not text or len(text.split()) < 100:
            return text
        prompt = f"Summarize the following artifact section in one paragraph:\n\n{text}"
        return chat_completion_request(prompt)

    def run(self, inputs):
        trace = []
        artifact = inputs.get("artifact")
        section = inputs.get("section")
        raw_feedback = inputs.get("feedback_text")
        mode = inputs.get("mode")
        session_id = inputs.get("session_id")
        user_id = inputs.get("user_id")
        project_id = inputs.get("project_id")

        # Step 1: memory
        memory_input = {**inputs}
        memory = self.memory_tool.run_tool(memory_input)
        log_tool_usage("memory_retrieve", "retrieved memory", memory, session_id, user_id, inputs)
        trace.append({"tool": "memory_retrieve", "output": memory})
        logger.info("[Step 1] memory_retrieve complete")

        # Step 2: feedback preprocessing
        preprocessed = self.feedback_preprocessor.run_tool({"feedback_text": raw_feedback})
        cleaned_feedback = preprocessed.get("cleaned_text", raw_feedback)
        raw_split = preprocessed.get("split_feedback", [cleaned_feedback])
        revision_type = preprocessed.get("inferred_type", mode)
        trace.append({"tool": "feedback_preprocessor", "output": preprocessed})
        logger.info("[Step 2] feedback_preprocessor complete")

        # Step 3: retrieve current section
        db = get_session()
        section_record = db.query(ArtifactSection).filter_by(artifact_id=artifact, section_id=section).order_by(ArtifactSection.timestamp.desc()).first()
        current_text = section_record.text if section_record else ""

        # Step 4: feedback logging
        save_feedback(document_id=artifact, feedback_text=raw_feedback, submitted_by=user_id, feedback_type="revision", project_id=project_id)

        # Fetch and summarize all artifact sections
        section_records = db.query(ArtifactSection).filter_by(artifact_id=artifact).order_by(ArtifactSection.timestamp.desc()).all()
        summarized_sections = []
        seen_sections = set()
        for sec in section_records:
            if sec.section_id not in seen_sections:
                summarized_sections.append({
                    "section_id": sec.section_id,
                    "text": self.summarize_text(sec.text)
                })
                seen_sections.add(sec.section_id)

        suggestions = []

        # Step 5: Manual edit path
        if revision_type == "verbatim":
            output = self.manual_edit_tool.run_tool({**inputs, "current_text": current_text})
            log_tool_usage("manualEditSync", "accepted user override", output, session_id, user_id, inputs)
            trace.append({"tool": "manualEditSync", "output": output})
            logger.info("[Step 3] manualEditSync complete")

            save_result = save_artifact_and_trace(
                section_id=section,
                artifact_id=artifact,
                gate_id=inputs.get("gate_id", "0"),
                text=raw_feedback,
                sources="manual user input",
                tool_outputs=trace,
                user_id=user_id,
                project_id=project_id
            )
            logger.info("[Step 5] Saved verbatim input to ArtifactSection and ReasoningTrace")
        else:
            for item in raw_split:
                if isinstance(item, dict):
                    fb = item.get("text")
                    fb_type = item.get("type", revision_type)
                else:
                    fb = item
                    fb_type = revision_type

                section_ids = [section] if section else []
                if not section:
                    map_result = self.feedback_mapper.run_tool({"feedback_text": fb, "sections": summarized_sections, **inputs})
                    section_ids = map_result.get("section_ids", [])
                    trace.append({"tool": "feedback_mapper", "output": map_result})
                    logger.info("[Step 3] feedback_mapper complete")

                for sec_id in section_ids:
                    rewritten = self.section_rewriter.run_tool({
                        "section_id": sec_id,
                        "memory": memory,
                        "feedback": fb,
                        "revision_type": fb_type,
                        "current_text": current_text,
                        **inputs
                    })
                    log_tool_usage("section_rewriter", "revised section", rewritten, session_id, user_id, inputs)
                    trace.append({"tool": "section_rewriter", "output": rewritten})
                    logger.info(f"[Step 4] section_rewriter complete for {sec_id}")

                    save_result = save_artifact_and_trace(
                        section_id=sec_id,
                        artifact_id=artifact,
                        gate_id=inputs.get("gate_id", "0"),
                        text=rewritten["draft"],
                        sources=rewritten.get("prompt_used"),
                        tool_outputs=trace,
                        user_id=user_id,
                        project_id=project_id
                    )
                    logger.info("[Step 5] Saved to ArtifactSection and ReasoningTrace")

                    if "additional_suggestions" in rewritten:
                        suggestions.append(rewritten["additional_suggestions"])

        return {"trace": trace, "status": "complete", "additional_suggestions": suggestions}