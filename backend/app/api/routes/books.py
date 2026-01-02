from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.api.routes.auth import get_current_user
from app.schemas.fichier_numerique import (
    FichierNumeriqueCreate, 
    FichierNumeriqueUpdate, 
    FichierNumeriqueSearch,
    FichierNumeriqueRead
)
from app.db.repositories.fichier_numerique_repository import FichierNumeriqueRepository
from app.db.models.fichier_numerique import Etat, FichierNumerique

router = APIRouter(prefix="/books", tags=["Books"])


# ============================================
# ROUTES PUBLIQUES (lecture)
# ============================================

@router.get("/", response_model=List[FichierNumeriqueRead])
async def lister_livres(
    db: Session = Depends(get_db)
):
    """Liste tous les livres disponibles (état = disponible)"""
    repo = FichierNumeriqueRepository(db)
    fichiers = repo.lister_fichiers()
    # Filtrer uniquement les disponibles pour le public
    return [f for f in fichiers if f.etat == Etat.DISPONIBLE]


@router.get("/{id_fichier}", response_model=FichierNumeriqueRead)
async def obtenir_livre(
    id_fichier: int,
    db: Session = Depends(get_db)
):
    """Obtenir un livre spécifique par son ID"""
    repo = FichierNumeriqueRepository(db)
    fichier = repo.get_by_id(id_fichier)
    
    if not fichier:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Livre non trouvé"
        )
    
    return fichier


@router.get("/search/", response_model=List[FichierNumeriqueRead])
async def rechercher_livres(
    titre: str = None,
    db: Session = Depends(get_db)
):
    """Rechercher des livres par titre"""
    repo = FichierNumeriqueRepository(db)
    
    if titre:
        return repo.search_by_title(titre)
    
    return repo.lister_fichiers()


# ============================================
# ROUTES PROTÉGÉES (membre/biblio/admin)
# ============================================

@router.post("/propose", response_model=FichierNumeriqueRead, status_code=status.HTTP_201_CREATED)
async def proposer_oeuvre(
    fichier_data: FichierNumeriqueCreate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Permet à un MEMBRE de proposer une œuvre stockée sur GitHub
    L'œuvre sera en état 'a_verifier' par défaut
    """
    # Vérifier que c'est au moins un membre
    if current_user.role not in ["membre", "bibliothecaire", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Vous devez être membre pour proposer une œuvre"
        )
    
    repo = FichierNumeriqueRepository(db)
    
    # Créer le modèle avec l'état à vérifier
    nouveau_fichier = FichierNumerique(
        titre=fichier_data.titre,
        chemin_github=fichier_data.chemin_github,
        type_fichier=fichier_data.type_fichier,
        categorie=fichier_data.categorie,
        domaine=fichier_data.domaine,
        etat=Etat.A_VERIFIER  # Toujours à vérifier au début
    )
    
    try:
        fichier_cree = repo.create(nouveau_fichier)
        return fichier_cree
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erreur lors de la création : {str(e)}"
        )


@router.get("/mes-propositions/", response_model=List[FichierNumeriqueRead])
async def mes_propositions(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Récupère toutes les œuvres proposées par le membre connecté
    (nécessiterait une relation user_id dans FichierNumerique pour être complet)
    """
    # TODO: Ajouter un champ user_id dans FichierNumerique pour tracer qui a proposé
    repo = FichierNumeriqueRepository(db)
    return repo.lister_fichiers()


# ============================================
# ROUTES ADMIN/BIBLIOTHÉCAIRE
# ============================================

@router.get("/admin/a-verifier", response_model=List[FichierNumeriqueRead])
async def lister_a_verifier(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Liste tous les livres en attente de vérification (pour biblio/admin)"""
    if current_user.role not in ["bibliothecaire", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès réservé aux bibliothécaires et administrateurs"
        )
    
    repo = FichierNumeriqueRepository(db)
    fichiers = repo.lister_fichiers()
    return [f for f in fichiers if f.etat == Etat.A_VERIFIER]


@router.patch("/{id_fichier}/valider", response_model=FichierNumeriqueRead)
async def valider_oeuvre(
    id_fichier: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Valide une œuvre (passe l'état à 'disponible')"""
    if current_user.role not in ["bibliothecaire", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès réservé aux bibliothécaires et administrateurs"
        )
    
    repo = FichierNumeriqueRepository(db)
    fichier = repo.get_by_id(id_fichier)
    
    if not fichier:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Livre non trouvé"
        )
    
    fichier_valide = repo.modifier_etat(fichier, Etat.DISPONIBLE)
    return fichier_valide


@router.patch("/{id_fichier}/rejeter", response_model=FichierNumeriqueRead)
async def rejeter_oeuvre(
    id_fichier: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Rejette une œuvre (passe l'état à 'indisponible')"""
    if current_user.role not in ["bibliothecaire", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès réservé aux bibliothécaires et administrateurs"
        )
    
    repo = FichierNumeriqueRepository(db)
    fichier = repo.get_by_id(id_fichier)
    
    if not fichier:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Livre non trouvé"
        )
    
    fichier_rejete = repo.modifier_etat(fichier, Etat.INDISPONIBLE)
    return fichier_rejete


@router.put("/{id_fichier}", response_model=FichierNumeriqueRead)
async def modifier_livre(
    id_fichier: int,
    fichier_update: FichierNumeriqueUpdate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Modifie un livre (admin/biblio uniquement)"""
    if current_user.role not in ["bibliothecaire", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès réservé aux bibliothécaires et administrateurs"
        )
    
    repo = FichierNumeriqueRepository(db)
    fichier = repo.get_by_id(id_fichier)
    
    if not fichier:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Livre non trouvé"
        )
    
    # Mise à jour des champs
    for key, value in fichier_update.dict(exclude_unset=True).items():
        setattr(fichier, key, value)
    
    fichier_modifie = repo.mettre_a_jour(fichier)
    return fichier_modifie


@router.delete("/{id_fichier}", status_code=status.HTTP_204_NO_CONTENT)
async def supprimer_livre(
    id_fichier: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Supprime un livre (admin uniquement)"""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès réservé aux administrateurs"
        )
    
    repo = FichierNumeriqueRepository(db)
    fichier = repo.get_by_id(id_fichier)
    
    if not fichier:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Livre non trouvé"
        )
    
    repo.supprimer(fichier)
    return None