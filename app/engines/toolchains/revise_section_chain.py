from app.engines.toolchains.base import BaseToolchain
from app.tools.tool_wrappers.feedback_mapper import Tool as FeedbackMapper
from app.tools.tool_wrappers.feedback_preprocessor import Tool as FeedbackPreprocessor
from app.tools.tool_wrappers.section_rewriter import Tool as SectionRewriter
from app.tools.tool_wrappers.revision_checker import Tool as RevisionChecker
from app.tools.tool_wrappers.manualEditSync import Tool as ManualEdit
from app.engines.memory_sync import save_artifact_and_trace, save_feedback
from app.db.models.ArtifactSection import ArtifactSection
from app.db.database import SessionLocal
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class ReviseSectionChain(BaseToolchain):
    def run(self, input_dict):
        session = SessionLocal()
        trace = []
        feedback = input_dict.get("feedback_text")
        section = input_dict.get("section")
        sections = input_dict.get("sections", [])

        # Step 1: Preprocess feedback
        pre_result = FeedbackPreprocessor().run_tool({"feedback_text": feedback})
        split_feedback = pre_result.get("split_feedback", [])
        revision_type = pre_result.get("inferred_type")
        trace.append({"tool": "feedback_preprocessor", "output": pre_result})

        # Prepare summarized sections
        db_sections = session.query(ArtifactSection).filter(
            ArtifactSection.section_id.in_(sections),
            ArtifactSection.artifact_id == input_dict["artifact"]
        ).all()

        summarized_sections = []
        for sec in db_sections:
            summary = sec.text[:400] + "..." if len(sec.text) > 400 else sec.text
            summarized_sections.append({"section_id": sec.section_id, "summary": summary})

        input_dict["sections"] = summarized_sections

        all_suggestions = []
        for fb in split_feedback:
            input_dict["feedback_text"] = fb
            section_ids = [section]
            if not section:
                map_result = FeedbackMapper().run_tool({"feedback_text": fb, **input_dict})
                section_ids = map_result.get("section_ids", [])
                trace.append({"tool": "feedback_mapper", "output": map_result})

            for sid in section_ids:
                if sid == "not_specified":
                    continue

                artifact_section = session.query(ArtifactSection).filter_by(section_id=sid, artifact_id=input_dict["artifact"]).first()
                if not artifact_section:
                    continue

                current_text = artifact_section.text

                if revision_type == "verbatim":
                    status = ManualEdit().run_tool({"section": sid, **input_dict})
                    trace.append({"tool": "manual_edit_sync", "output": status})
                else:
                    rewrite = SectionRewriter().run_tool({
                        "section_id": sid,
                        "feedback": fb,
                        "revision_type": revision_type,
                        "current_text": current_text
                    })
                    trace.append({"tool": "section_rewriter", "output": rewrite})

                    check = RevisionChecker().run_tool({
                        "original_text": current_text,
                        "revised_text": rewrite["draft"],
                        "revision_type": revision_type
                    })
                    trace.append({"tool": "revision_checker", "output": check})

                    save_artifact_and_trace(
                        section_id=sid,
                        new_text=rewrite["draft"],
                        trace_log=trace,
                        input_dict=input_dict
                    )

                    if rewrite.get("additional_suggestions"):
                        all_suggestions.extend(rewrite["additional_suggestions"])

                save_feedback(
                    artifact=input_dict.get("artifact"),
                    section_id=sid,
                    user_id=input_dict.get("user_id"),
                    feedback_text=fb,
                    project_id=input_dict.get("project_id"),
                    session_id=input_dict.get("session_id")
                )

        return {"status": "complete", "additional_suggestions": all_suggestions}