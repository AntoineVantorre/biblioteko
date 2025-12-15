from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from schemas.utilisateur import UtilisateurBase, UtilisateurCreate, UtilisateurRead, UtilisateurUpdate, MembreCreate, BibliothecaireCreate
from schemas.fichier_numerique import FichierNumeriqueBase, FichierNumeriqueCreate, FichierNumeriqueUpdate, FichierNumeriqueSearch

from app.services.utilisateur_service import UtilisateurService

router = APIRouter(prefix="/users", tags=["Users"])

async def get_current_db(db=Depends(get_db)):
    return db

@router.post("/", response_model=UtilisateurRead)
async def create_user(
    utilisateur: UtilisateurCreate,
    db: Session = Depends(get_current_db)
):
    utilisateur_service = UtilisateurService(db)
    return utilisateur_service.create_utilisateur(utilisateur)
