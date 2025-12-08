from typing import List, Optional
from sqlmodel import Session, select
from db.models.fichier_numerique import FichierNumerique

class FichierNumeriqueRepository:
    def __init__(self, session: Session):
        self.session = session

    # --- Create ---
    def create(self, fichier: FichierNumerique) -> FichierNumerique:
        self.session.add(fichier)
        self.session.commit()
        self.session.refresh(fichier)  # récupère l'ID généré
        return fichier

    # --- Read ---
    def get_by_id(self, id_fichier: int) -> Optional[FichierNumerique]:
        return self.session.get(FichierNumerique, id_fichier)

    def get_all(self) -> List[FichierNumerique]:
        return self.session.exec(select(FichierNumerique)).all()

    def get_by_categorie(self, categorie: str) -> List[FichierNumerique]:
        return self.session.exec(
            select(FichierNumerique).where(FichierNumerique.categorie == categorie)
        ).all()

    # --- Update ---
    def update(self, fichier: FichierNumerique) -> FichierNumerique:
        self.session.add(fichier)
        self.session.commit()
        self.session.refresh(fichier)
        return fichier

    # --- Delete ---
    def delete(self, fichier: FichierNumerique) -> None:
        self.session.delete(fichier)
        self.session.commit()
