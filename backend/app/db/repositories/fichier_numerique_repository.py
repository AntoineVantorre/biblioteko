from typing import List, Optional
from sqlmodel import Session, select
from app.db.models.fichier_numerique import FichierNumerique, Etat


class FichierNumeriqueRepository:
    """Repository pour gérer les opérations CRUD sur les fichiers numériques."""
    
    def __init__(self, session: Session):
        self.session = session

    # -----------------------------
    # CREATE
    # -----------------------------
    def create(self, fichier_model: FichierNumerique) -> FichierNumerique:
        self.session.add(fichier_model)
        self.session.commit()
        self.session.refresh(fichier_model)
        return fichier_model

    # -----------------------------
    # READ
    # -----------------------------
    def get_by_id(self, id_fichier: int) -> Optional[FichierNumerique]:
        return self.session.get(FichierNumerique, id_fichier)

    def search_by_title(self, nom: str) -> List[FichierNumerique]:
        statement = select(FichierNumerique).where(FichierNumerique.titre.ilike(f"%{nom}%"))
        return self.session.exec(statement).all()

    def lister_fichiers(self) -> List[FichierNumerique]:
        return self.session.exec(select(FichierNumerique)).all()

    # -----------------------------
    # UPDATE
    # -----------------------------
    def mettre_a_jour(
        self,
        fichiernow: FichierNumerique,
    ) -> FichierNumerique:

        data = fichiernow.model_dump(exclude_unset=True)
        fichierbefore = self.get_by_id(fichiernow.id_fichier)

        for key, value in data.items():
            setattr(fichierbefore, key, value)

        self.session.add(fichiernow)
        self.session.commit()
        self.session.refresh(fichiernow)
        return fichiernow

    def modifier_etat(
        self,
        fichier: FichierNumerique,
        nouvel_etat: Etat
    ) -> FichierNumerique:

        fichier.etat = nouvel_etat
        self.session.add(fichier)
        self.session.commit()
        self.session.refresh(fichier)
        return fichier

    # -----------------------------
    # DELETE
    # -----------------------------
    def supprimer(self, fichier: FichierNumerique):
        self.session.delete(fichier)
        self.session.commit()