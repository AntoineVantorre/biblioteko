from datetime import datetime
from pydantic import EmailStr
from sqlmodel import SQLModel, Field, Index

class Utilisateur(SQLModel, table=True):
    id_utilisateur: int = Field(default=None, primary_key=True)
    prenom: str = Field(..., min_length=1)
    nom: str = Field(..., min_length=1)
    email: EmailStr = Field(..., unique=True)
    mot_de_passe: str  #ici on stock le hash du mot de passe
    date_inscription: datetime = Field(default_factory=datetime.now) #obligatoire pour le RGPD
    role: str = Field(default="utilisateur", pattern="^(utilisateur|membre|bibliothecaire|admin)$")

    def est_admin(self) -> bool:
        return self.role == "admin"

    def est_bibliothecaire(self) -> bool:
        return self.role == "bibliothecaire"

    def est_membre(self) -> bool:
        return self.role == "membre"
    

# -------------------------------------------------
# Sous-classe : Membre
# -------------------------------------------------
class Membre(Utilisateur):
    liste_emprunts: Optional[List[str]] = None
    propositions_oeuvres: Optional[List[str]] = None

    def proposer_oeuvre(self, oeuvre_id: str):
        if self.role != "membre":
            raise PermissionError("Seulement les membres peuvent proposer des œuvres")
        if self.propositions_oeuvres is None:
            self.propositions_oeuvres = []
        self.propositions_oeuvres.append(oeuvre_id)

    def consulter_emprunts(self):
        return self.liste_emprunts or []

# -------------------------------------------------
# Sous-classe : Bibliothecaire
# -------------------------------------------------
class Bibliothecaire(Membre):
    permissions_moderation: Optional[List[str]] = None

    def valider_oeuvre(self, oeuvre_id: str):
        if self.role != "bibliothecaire":
            raise PermissionError("Seulement les bibliothécaires peuvent valider des œuvres")
        # logique de validation
        if self.permissions_moderation is None:
            self.permissions_moderation = []
        self.permissions_moderation.append(oeuvre_id)

    def rejeter_oeuvre(self, oeuvre_id: str):
        # logique de rejet
        pass

    def corriger_metadonnees(self, oeuvre_id: str):
        # logique correction
        pass

# -------------------------------------------------
# Sous-classe : Administrateur
# -------------------------------------------------
class Administrateur(Utilisateur):
    permissions_admin: Optional[List[str]] = None

    def gerer_utilisateurs(self):
        # logique de gestion
        pass

    def auditer_systeme(self):
        # logique audit
        pass

    def supprimer_oeuvre(self, oeuvre_id: str):
        if self.permissions_admin is None:
            self.permissions_admin = []
        self.permissions_admin.append(oeuvre_id)