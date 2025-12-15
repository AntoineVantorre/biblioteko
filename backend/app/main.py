from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
from fastapi import APIRouter

# import the transcribe router (added below)
from app.api.routes import transcribe as transcribe_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/hello")
def hello():
    return {"msg": "Hello API"}


# Include transcribe router
app.include_router(transcribe_router.router, prefix="/api")

# Servir les assets (JS, CSS, etc.)
app.mount("/assets", StaticFiles(directory="/app/dist/assets"), name="assets")

# Route catch-all pour le SPA (doit être en dernier)
@app.get("/{full_path:path}")
async def serve_spa(full_path: str):
    file_path = f"/app/dist/{full_path}"
    if os.path.exists(file_path) and os.path.isfile(file_path):
        return FileResponse(file_path)
    return FileResponse("/app/dist/index.html")