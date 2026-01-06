from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel

# Import de la configuration
from app.config import settings

# Import de la base de données
from app.db.session import engine

# Import des routes
from app.api.routes import transcribe as transcribe_router
from app.api.routes import auth, books

# ============================================
# GESTION DU CYCLE DE VIE (LIFESPAN)
# ============================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gestionnaire de démarrage et d'arrêt de l'application.
    Remplace les anciens @app.on_event("startup") et "shutdown".
    """
    # --- PHASE DE DÉMARRAGE (STARTUP) ---
    print(f"🚀 {settings.APP_NAME} v{settings.APP_VERSION} en cours de démarrage...")
    
    try:
        # Crée les tables dans la BDD si elles n'existent pas
        # C'est ici que la connexion à "db" est testée
        SQLModel.metadata.create_all(engine)
        print("✅ Base de données connectée et tables vérifiées.")
    except Exception as e:
        print(f"❌ Erreur lors de la connexion à la base de données : {e}")
        # On ne stoppe pas forcément l'app, mais les routes BDD échoueront

    print(f"📚 Documentation disponible sur : http://localhost:8000/docs")
    
    yield  # L'application tourne et accepte des requêtes ici
    
    # --- PHASE D'ARRÊT (SHUTDOWN) ---
    print("👋 Arrêt de l'application")


# ============================================
# CRÉATION DE L'APPLICATION
# ============================================
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    lifespan=lifespan  # On lie le lifespan ici
)

# ============================================
# MIDDLEWARE CORS
# ============================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
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