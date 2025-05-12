from fastapi import FastAPI
from app.tools import (
    get_triage_flow,
    get_triage_question,
    log_incident_detail,
    assess_concussion,
    symptom_logger,
    get_stage_guidance,
    export_summary
)

app = FastAPI(
    title="Concussion Recovery App – GPT Tools",
    version="1.0.0",
    description="Tools for triage, symptom tracking, stage guidance, and export in a concussion recovery GPT."
)

# Register routers
app.include_router(get_triage_flow.router)
app.include_router(get_triage_question.router)
app.include_router(log_incident_detail.router)
app.include_router(assess_concussion.router)
app.include_router(symptom_logger.router)
app.include_router(get_stage_guidance.router)
app.include_router(export_summary.router)  # Non-async tools like export_to_sql are CLI-only

@app.get("/openapi.json")
def get_openapi_schema():
    return app.openapi()