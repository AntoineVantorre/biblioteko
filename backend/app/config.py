import os
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """Configuration de l'application"""
    
    # Application
    APP_NAME: str = "Bibliothèque Numérique"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # URLs
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:5173")
    
    # Base de données PostgreSQL
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://user:password@localhost:5432/bibliotheque_db"
    )
    
    # Sécurité JWT
    SECRET_KEY: str = os.getenv(
        "SECRET_KEY",
        "CHANGE_ME_IN_PRODUCTION_USE_OPENSSL_RAND_HEX_32"
    )
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # CORS - Frontend URLs autorisées
    CORS_ORIGINS: list = [
        "http://localhost:5173",  # Vite dev server
        "http://localhost:3000",  # Alternative
        "http://localhost:8080",  # Alternative
    ]
    
    # Email SMTP - Utilise vos noms de variables existants
    SMTP_HOST: str = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    SMTP_PORT: int = int(os.getenv("MAIL_PORT", "587"))
    SMTP_USER: str = os.getenv("MAIL_USERNAME", "votre_email@gmail.com")
    SMTP_PASSWORD: str = os.getenv("MAIL_PASSWORD", "votre_mot_de_passe_app")
    FROM_EMAIL: str = os.getenv("MAIL_FROM", os.getenv("MAIL_USERNAME", "votre_email@gmail.com"))
    FROM_NAME: str = os.getenv("FROM_NAME", "Bibliothèque Numérique")
    
    # FranceConnect OAuth2
    FRANCE_CONNECT_CLIENT_ID: str = os.getenv("FRANCE_CONNECT_CLIENT_ID", "")
    FRANCE_CONNECT_CLIENT_SECRET: str = os.getenv("FRANCE_CONNECT_CLIENT_SECRET", "")
    FRANCE_CONNECT_REDIRECT_URI: str = os.getenv(
        "FRANCE_CONNECT_REDIRECT_URI",
        "http://localhost:8000/api/auth/franceconnect/callback"
    )
    # URLs FranceConnect (environnement de test)
    FRANCE_CONNECT_AUTHORIZE_URL: str = "https://fcp.integ01.dev-franceconnect.fr/api/v1/authorize"
    FRANCE_CONNECT_TOKEN_URL: str = "https://fcp.integ01.dev-franceconnect.fr/api/v1/token"
    FRANCE_CONNECT_USERINFO_URL: str = "https://fcp.integ01.dev-franceconnect.fr/api/v1/userinfo"
    
    # GitHub (pour stocker les fichiers)
    GITHUB_TOKEN: Optional[str] = os.getenv("GITHUB_TOKEN")
    GITHUB_REPO: str = os.getenv("GITHUB_REPO", "username/repo")  # Format: owner/repo
    GITHUB_BRANCH: str = os.getenv("GITHUB_BRANCH", "main")
    
    # Uploads
    MAX_FILE_SIZE_MB: int = 50  # Taille max des fichiers en MB
    ALLOWED_FILE_TYPES: list = ["pdf", "epub", "mp3", "mp4", "jpg", "png"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Instance globale des settings
settings = Settings()