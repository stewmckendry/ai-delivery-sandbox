from fastapi import FastAPI
from fastapi.requests import Request

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
from app.tools.get_user_history import router as history_router
from app.tools.log_checkin_gptfix import router as checkin_gptfix_router

app = FastAPI()

@app.middleware("http")
async def log_request_body(request: Request, call_next):
    try:
        body = await request.body()
        print(f"\n📥 Incoming Request: {request.method} {request.url.path}")
        print(f"🔍 Body: {body.decode('utf-8')}")
    except Exception as e:
        print(f"⚠️ Error reading request body: {e}")
    return await call_next(request)

app.include_router(triage_router)
app.include_router(incident_router)
#app.include_router(symptom_map_router) - deprecated, replaced by checkin_flow
#app.include_router(symptom_logger_router) - deprecated, replaced by activity_checkin
app.include_router(assess_router)
app.include_router(stage_router)
app.include_router(export_router)
#app.include_router(linked_router) - deprecated, replaced by history
app.include_router(activity_checkin_router)
app.include_router(overview_router)
app.include_router(checkin_flow_router)
app.include_router(history_router)
app.include_router(checkin_gptfix_router)