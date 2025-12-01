from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api.routes import auth_router

app = FastAPI()

# 1) API routes
app.include_router(auth_router, prefix="/auth")
@app.get("/api/hello")
def hello():
    return {"msg": "Hello API"}

# 2) Frontend SPA
# Toutes les routes non-API renvoient index.html
app.mount("/", StaticFiles(directory="/app/dist", html=True), name="frontend")
