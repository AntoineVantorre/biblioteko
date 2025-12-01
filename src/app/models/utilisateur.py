from beanie import Document
from datetime import datetime
from typing import Optional
from pydantic import EmailStr, Field


class Utilisateur(Document):
    prenom: str = Field(..., min_length=1)
    nom: str = Field(..., min_length=1)
    email: EmailStr
    mot_de_passe: str  #ici on stock le hash du mot de passe
    date_inscription: datetime = Field(default_factory=datetime.now) #obligatoire pour le RGPD

    role: str = Field(default="membre", regex="^(membre|bibliothecaire|admin)$")

    class Settings:
        name = "utilisateurs"   # nom de la collection MongoDB

    def est_admin(self) -> bool:
        return self.role == "admin"

    def est_bibliothecaire(self) -> bool:
        return self.role == "bibliothecaire"

    def est_membre(self) -> bool:
        return self.role == "membre"
