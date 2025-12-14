from typing import List, Optional

from pydantic import BaseModel

from app.db.repositories.fichier_numerique_repository import FichierNumeriqueRepository
from app.db.models.fichier_numerique import FichierNumerique, Etat
from app.db.models.utilisateur import Utilisateur
from app.schemas.fichier_numerique import FichierNumeriqueCreate, FichierNumeriqueBase, Domaine, Categorie

class UtilisateurService:
    def __init__(self, fichier_repo: FichierNumeriqueRepository):
        self.fichier_repo = fichier_repo

    def consulter_oeuvre_par_id(
        self,
        utilisateur: Utilisateur,
        fichier_id: int
    ) -> Optional[FichierNumerique]:

            fichier_model = self.fichier_repo.get_fichier_par_id(fichier_id)

            if not fichier_model:
                return None

            if fichier_model.etat != Etat.DISPONIBLE:
                raise PermissionError("Cette œuvre n'est pas disponible")
            return FichierNumeriqueBase(**fichier_model.model_dump())


    def rechercher_oeuvres_disponibles_par_titre(
        self,
        utilisateur: Utilisateur,
        titre: str
    ) -> List[FichierNumeriqueBase]:

        fichiers = self.fichier_repo.chercher_par_nom(titre)

        return [
            FichierNumeriqueBase(**f.model_dump()) for f in fichiers
            if f.etat == Etat.DISPONIBLE
        ]
    
    def recherche_oeuvres_par_titre(
            self,
            utilisateur: Utilisateur,  #l'utilisateur qui appelle cette fonction
            titre: str                 # l'oeuvre recherchée
    ) -> List[FichierNumeriqueBase]:
        
        fichiers = self.fichier_repo.chercher_par_nom(titre)

        return fichiers

    def proposer_oeuvre(
        self,
        utilisateur: Utilisateur,
        fichier: FichierNumeriqueBase
    ):

        if not utilisateur.est_membre():
            raise PermissionError("Seuls les membres peuvent proposer des œuvres")

        fichier.etat = Etat.A_VERIFIER

        return self.fichier_repo.create(fichier)
