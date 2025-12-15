from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


# ==========================================================
#  Base commune à tous les schémas utilisateur
# ==========================================================

class UtilisateurBase(BaseModel):
    prenom: str = Field(..., min_length=1)
    nom: str = Field(..., min_length=1)
    email: EmailStr
    role: str = Field(
        default="utilisateur",
        pattern="^(utilisateur|membre|bibliothecaire|admin)$"
    )


# ==========================================================
#  Schemas utilisés pour créer un utilisateur
# ==========================================================

class UtilisateurCreate(UtilisateurBase):
    mot_de_passe: str = Field(..., min_length=6)


# ==========================================================
#  Schemas pour mettre à jour un utilisateur
# ==========================================================

class UtilisateurUpdate(BaseModel):
    prenom: Optional[str]
    nom: Optional[str]
    email: Optional[EmailStr]
    role: Optional[str]
    mot_de_passe: Optional[str]


# ==========================================================
#  Schéma retourné par l'API (sans mot de passe)
# ==========================================================

class UtilisateurRead(UtilisateurBase):
    id_utilisateur: int
    date_inscription: datetime

    class Config:
        from_attributes = True 


# ==========================================================
#  Schémas spécifiques pour les rôles
# ==========================================================

class MembreRead(UtilisateurRead):
    liste_emprunts: Optional[list[str]] = None
    propositions_oeuvres: Optional[list[str]] = None


class BibliothecaireRead(UtilisateurRead):
    permissions_moderation: Optional[list[str]] = None


class AdministrateurRead(UtilisateurRead):
    permissions_admin: Optional[list[str]] = None
