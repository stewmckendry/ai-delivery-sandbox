import json
import uuid
import datetime
from app.db.database import get_session
from app.db.models.ArtifactSection import ArtifactSection
from app.db.models.ReasoningTrace import ReasoningTrace
from app.db.models.PromptLog import PromptLog
from sqlalchemy.orm import Session


def save_artifact_and_trace(section_id, artifact_id, gate_id, text, sources, tool_outputs, user_id):
    session = get_session()

    artifact = ArtifactSection(
        section_id=section_id,
        artifact_id=artifact_id,
        gate_id=gate_id,
        text=text,
        sources=sources,
        status="draft",
        generated_by="generate_section",
        timestamp=datetime.datetime.utcnow()
    )

    trace = ReasoningTrace(
        trace_id=str(uuid.uuid4()),
        section_id=section_id,
        steps=tool_outputs,
        created_by=user_id,
        created_at=datetime.datetime.utcnow()
    )

    session.add(artifact)
    session.add(trace)
    session.commit()
    return {"section_id": section_id, "trace_id": trace.trace_id}


def log_tool_usage(tool_name, input_summary, output_summary, session_id, user_id=None, metadata=None):
    db: Session = get_session()

    output_summary_str = json.dumps(output_summary) if isinstance(output_summary, (dict, list)) else str(output_summary)
    full_input = json.dumps(metadata, indent=2) if metadata else None
    full_output = json.dumps(output_summary, indent=2) if isinstance(output_summary, (dict, list)) else str(output_summary)

    prompt_log = PromptLog(
        tool=tool_name,
        input_summary=str(input_summary),
        output_summary=output_summary_str,
        full_input_path=full_input,
        full_output_path=full_output,
        session_id=session_id,
        user_id=user_id,
        timestamp=datetime.datetime.utcnow(),
    )

    db.add(prompt_log)
    db.commit()
    db.refresh(prompt_log)

    return prompt_log.id