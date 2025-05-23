from app.db.models.ArtifactSection import ArtifactSection
from app.db.models.ReasoningTrace import ReasoningTrace
from app.db.database import get_session
import uuid
import datetime


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