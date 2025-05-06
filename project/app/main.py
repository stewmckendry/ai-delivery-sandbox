from fastapi import FastAPI, Depends
from project.app.routes import memory, prompts, segments
from project.app.utils.auth import verify_token

app = FastAPI()

app.include_router(memory.router, dependencies=[Depends(verify_token)])
app.include_router(prompts.router, dependencies=[Depends(verify_token)])
app.include_router(segments.router, dependencies=[Depends(verify_token)])

@app.get("/")
async def root():
    return {"message": "CareerCoach API is live"}