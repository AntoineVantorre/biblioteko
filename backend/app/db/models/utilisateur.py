from datetime import datetime
from pydantic import EmailStr
from sqlmodel import SQLModel, Field, Index
from typing import List, Optional


class Utilisateur(SQLModel, table=True):
    id_utilisateur: int = Field(default=None, primary_key=True)
    prenom: str = Field(..., min_length=1)
    nom: str = Field(..., min_length=1)
    email: EmailStr = Field(..., unique=True)
    mot_de_passe: str  #ici on stock le hash du mot de passe
    date_inscription: datetime = Field(default_factory=datetime.now) #obligatoire pour le RGPD
    role: str = Field(default="utilisateur", pattern="^(utilisateur|membre|bibliothecaire|admin)$")
    propositions_oeuvres: Optional[List[int]] = Field(default_factory=list, sa_column=Index("idx_propositions_oeuvres"))

    def est_admin(self) -> bool:
        return self.role == "admin"

    def est_bibliothecaire(self) -> bool:
        return self.role == "bibliothecaire"

    def est_membre(self) -> bool:
        return self.role == "membre"
    