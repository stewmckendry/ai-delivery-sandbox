from fastapi import FastAPI
from app.tools.get_triage_flow import router as triage_router
from app.tools.log_incident_detail import router as incident_router
from app.tools.get_symptom_log_map import router as symptom_map_router
from app.tools.symptom_logger import router as symptom_logger_router
from app.tools.assess_concussion import router as assess_router
from app.tools.get_stage_guidance import router as stage_router
from app.tools.export_summary import router as export_router
from app.tools.get_linked_symptoms import router as linked_router
from app.tools.log_activity_checkin import router as activity_checkin_router
from app.tools.get_stage_overview import router as overview_router
from app.tools.get_checkin_flow import router as checkin_flow_router

app = FastAPI()

app.include_router(triage_router)
app.include_router(incident_router)
app.include_router(symptom_map_router)
app.include_router(symptom_logger_router)
app.include_router(assess_router)
app.include_router(stage_router)
app.include_router(export_router)
app.include_router(linked_router)
app.include_router(activity_checkin_router)
app.include_router(overview_router)
app.include_router(checkin_flow_router)