from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field


class Utilisateur(SQLModel, table=True):
    """Modèle de base pour tous les utilisateurs"""
    
    __tablename__ = "utilisateurs"
    
    id_utilisateur: Optional[int] = Field(default=None, primary_key=True)
    
    # Informations personnelles
    prenom: str = Field(min_length=1, max_length=100)
    nom: str = Field(min_length=1, max_length=100)
    email: str = Field(unique=True, index=True, max_length=255)
    mot_de_passe: str = Field(min_length=6)
    
    # Rôle : utilisateur, membre, bibliothecaire, admin
    role: str = Field(
        default="utilisateur",
        regex="^(utilisateur|membre|bibliothecaire|admin)$"
    )
    
    # Vérification email
    email_verifie: bool = Field(default=False)
    code_verification: Optional[str] = Field(default=None, max_length=6)
    code_expiration: Optional[datetime] = Field(default=None)
    
    # FranceConnect
    france_connect_id: Optional[str] = Field(default=None, unique=True, max_length=255)
    
    # Dates
    date_inscription: datetime = Field(default_factory=datetime.utcnow)
    derniere_connexion: Optional[datetime] = Field(default=None)
    
    class Config:
        arbitrary_types_allowed = True


class Membre(Utilisateur):
    """Membre avec droits de proposition d'œuvres"""
    pass


class Bibliothecaire(Utilisateur):
    """Bibliothécaire avec droits de modération"""
    pass


class Administrateur(Utilisateur):
    """Administrateur avec tous les droits"""
    pass