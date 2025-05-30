import json
import uuid
import datetime
from decimal import Decimal
from app.db.database import get_session
from app.db.models.ArtifactSection import ArtifactSection
from app.db.models.ReasoningTrace import ReasoningTrace
from app.db.models.PromptLog import PromptLog
from app.db.models.DocumentVersionLog import DocumentVersionLog
from app.db.models.DocumentFeedback import DocumentFeedback
from app.engines.project_profile_engine import ProjectProfileEngine
from sqlalchemy.orm import Session
from uuid import uuid4


def save_artifact_and_trace(section_id, artifact_id, gate_id, text, sources, tool_outputs, user_id, project_id=None, session_id=None):
    session = get_session()

    draft_chunks = None
    for step in tool_outputs:
        output = step.get("output", {})
        if isinstance(output, dict) and output.get("draft_chunks"):
            draft_chunks = output["draft_chunks"]
            break

    for step in tool_outputs:
        step["tool_version"] = output.get("tool_version", "v1")
        step["schema_version"] = output.get("schema_version", "1.0")

    artifact = ArtifactSection(
        section_id=section_id,
        artifact_id=artifact_id,
        gate_id=gate_id,
        text=text,
        sources=sources,
        status="draft",
        generated_by="generate_section",
        timestamp=datetime.datetime.utcnow(),
        project_id=project_id,
        session_id=session_id
    )

    trace = ReasoningTrace(
        trace_id=str(uuid.uuid4()),
        section_id=section_id,
        steps=json.dumps(tool_outputs),
        created_by=user_id,
        created_at=datetime.datetime.utcnow(),
        draft_chunks=json.dumps(draft_chunks) if draft_chunks else None,
        project_id=project_id
    )

    session.add(artifact)
    session.add(trace)
    session.commit()
    return {"section_id": section_id, "trace_id": trace.trace_id}


def save_feedback(document_id, feedback_text, submitted_by, feedback_type="general", project_id=None):
    session = get_session()
    feedback_entry = DocumentFeedback(
        document_id=document_id,
        feedback_text=feedback_text,
        submitted_by=submitted_by,
        feedback_type=feedback_type,
        status="open",
        created_at=datetime.datetime.utcnow(),
        project_id=project_id
    )
    session.add(feedback_entry)
    session.commit()
    return feedback_entry.document_feedback_id


def log_tool_usage(tool_name, input_summary, output_summary, session_id, user_id=None, metadata=None):
    db: Session = get_session()

    def convert(obj):
        if isinstance(obj, (datetime.datetime, datetime.date)):
            return obj.isoformat()
        if isinstance(obj, Decimal):
            return float(obj)
        raise TypeError(f"Type {type(obj)} not serializable")

    output_summary_str = json.dumps(output_summary, default=convert) if isinstance(output_summary, (dict, list)) else str(output_summary)
    full_input = json.dumps(metadata, indent=2, default=convert) if metadata else None
    full_output = json.dumps(output_summary, indent=2, default=convert) if isinstance(output_summary, (dict, list)) else str(output_summary)

    project_id = None
    if metadata:
        project_id = metadata.get("project_id") or metadata.get("project_profile", {}).get("project_id")

    prompt_log = PromptLog(
        tool=tool_name,
        input_summary=str(input_summary),
        output_summary=output_summary_str,
        full_input_path=full_input,
        full_output_path=full_output,
        session_id=session_id,
        user_id=user_id,
        timestamp=datetime.datetime.utcnow(),
        project_id=project_id
    )

    db.add(prompt_log)
    db.commit()
    db.refresh(prompt_log)

    return prompt_log.id


def save_document_and_trace(session_id, artifact_id, gate_id, version, storage_url, summary, inputs, output_path, tool_outputs):
    session = get_session()

    for step in tool_outputs:
        output = step.get("output", {})
        step["tool_version"] = output.get("tool_version", "v1")
        step["schema_version"] = output.get("schema_version", "1.0")

    project_id = inputs.get("project_id") or inputs.get("project_profile", {}).get("project_id")

    doc_log = DocumentVersionLog(
        doc_version_id=f"{project_id}_{artifact_id}_{str(uuid4())[:5]}",
        artifact_name=artifact_id,
        gate=int(gate_id),
        version_tag=version,
        submitted_by="assemble_artifact",
        file_path=output_path,
        google_doc_url=storage_url,
        doc_format="markdown",
        submitted_at=datetime.datetime.utcnow(),
        project_id=project_id,
        session_id=session_id
    )
    session.add(doc_log)

    trace = ReasoningTrace(
        trace_id=session_id,
        section_id=f"{artifact_id}:{gate_id}",
        steps=json.dumps(tool_outputs),
        created_by="assemble_artifact",
        created_at=datetime.datetime.utcnow(),
        draft_chunks=None,
        project_id=project_id
    )
    session.add(trace)
    session.commit()


def save_project_profile(profile_dict):
    return ProjectProfileEngine().save_profile(profile_dict)


def load_project_profile(project_id):
    return ProjectProfileEngine().load_profile(project_id)
