from fastapi import FastAPI
from project.app.routes import memory, prompts, segments

app = FastAPI()

app.include_router(memory.router)
app.include_router(prompts.router)
app.include_router(segments.router)

@app.get("/")
async def root():
    return {"message": "CareerCoach API is live"}