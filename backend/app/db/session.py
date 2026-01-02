from sqlmodel import Session, create_engine, SQLModel
from app.config import settings

# 1. On crée le moteur (Engine) qui gère la connexion physique
# On récupère l'URL de la base depuis ton fichier .env / config
engine = create_engine(
    settings.DATABASE_URL, 
    echo=True  # Affiche les requêtes SQL dans la console (pratique en dev)
)

# 2. La fonction get_db que ton fichier auth.py essaie d'importer
def get_db():
    """Générateur de session de base de données"""
    with Session(engine) as session:
        yield session  # On "donne" la session à la route
    # Une fois que la route a fini, le bloc "with" ferme la session automatiquement