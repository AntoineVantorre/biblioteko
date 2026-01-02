from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import de la configuration
from app.config import settings

# Import des routes
from app.api.routes import transcribe as transcribe_router
from app.api.routes import auth, books

# Créer l'application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG
)

# ============================================
# CORS - IMPORTANT pour front/back séparés
# ============================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,  # URLs autorisées depuis config.py
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================
# ROUTES API
# ============================================

@app.get("/")
def root():
    """Route racine - Info API"""
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "message": "API Backend - Frontend séparé"
    }

@app.get("/api/hello")
def hello():
    """Route de test"""
    return {"msg": "Hello API"}

# Enregistrer les routers
app.include_router(auth.router, prefix="/api")
app.include_router(books.router, prefix="/api")
app.include_router(transcribe_router.router, prefix="/api")

# ============================================
# ÉVÉNEMENTS
# ============================================

@app.on_event("startup")
async def startup_event():
    """Événement au démarrage"""
    print(f"🚀 {settings.APP_NAME} v{settings.APP_VERSION} démarré")
    print(f"📚 Documentation disponible sur : http://localhost:8000/docs")

@app.on_event("shutdown")
async def shutdown_event():
    """Événement à l'arrêt"""
    print("👋 Arrêt de l'application")