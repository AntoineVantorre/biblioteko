from typing import List, Optional
from sqlmodel import Session, select
from sqlalchemy import or_

from app.db.models.utilisateur import Utilisateur, Membre, Bibliothecaire, Administrateur


class UtilisateurRepository:
    """Repository pour gérer les opérations CRUD sur les utilisateurs."""
    
    def __init__(self, session: Session):
        self.session = session
    
    # -------------------------------------------------
    # CREATE
    # -------------------------------------------------
    def creer_utilisateur(self, utilisateur: Utilisateur) -> Utilisateur:
        """Créer un nouvel utilisateur en base de données."""
        try:
            self.session.add(utilisateur)
            self.session.commit()
            self.session.refresh(utilisateur)
            return utilisateur
        except Exception as e:
            self.session.rollback()
            raise ValueError(f"Erreur lors de la création de l'utilisateur : {str(e)}")
    
    # -------------------------------------------------
    # READ
    # -------------------------------------------------
    def obtenir_par_id(self, id_utilisateur: int) -> Optional[Utilisateur]:
        """Récupérer un utilisateur par son ID."""
        statement = select(Utilisateur).where(Utilisateur.id_utilisateur == id_utilisateur)
        return self.session.exec(statement).first()
    
    def obtenir_par_email(self, email: str) -> Optional[Utilisateur]:
        """Récupérer un utilisateur par son email."""
        statement = select(Utilisateur).where(Utilisateur.email == email)
        return self.session.exec(statement).first()
    
    def rechercher_par_nom(self, nom_partiel: str) -> List[Utilisateur]:
        """Rechercher des utilisateurs par nom partiel (insensible à la casse)."""
        statement = select(Utilisateur).where(
            or_(
                Utilisateur.nom.ilike(f"%{nom_partiel}%"),
                Utilisateur.prenom.ilike(f"%{nom_partiel}%")
            )
        )
        return self.session.exec(statement).all()
    
    def obtenir_tous(self) -> List[Utilisateur]:
        """Récupérer tous les utilisateurs."""
        statement = select(Utilisateur)
        return self.session.exec(statement).all()
    
    def obtenir_par_role(self, role: str) -> List[Utilisateur]:
        """Récupérer tous les utilisateurs avec un rôle spécifique."""
        statement = select(Utilisateur).where(Utilisateur.role == role)
        return self.session.exec(statement).all()
    
    # -------------------------------------------------
    # UPDATE
    # -------------------------------------------------
    def mettre_a_jour(self, id_utilisateur: int, donnees: dict) -> Optional[Utilisateur]:
        """Mettre à jour un utilisateur."""
        utilisateur = self.obtenir_par_id(id_utilisateur)
        if not utilisateur:
            return None
        
        for cle, valeur in donnees.items():
            if hasattr(utilisateur, cle) and valeur is not None:
                setattr(utilisateur, cle, valeur)
        
        try:
            self.session.add(utilisateur)
            self.session.commit()
            self.session.refresh(utilisateur)
            return utilisateur
        except Exception as e:
            self.session.rollback()
            raise ValueError(f"Erreur lors de la mise à jour : {str(e)}")
    
    # -------------------------------------------------
    # DELETE
    # -------------------------------------------------
    def supprimer(self, id_utilisateur: int) -> bool:
        """Supprimer un utilisateur par son ID."""
        utilisateur = self.obtenir_par_id(id_utilisateur)
        if not utilisateur:
            return False
        
        try:
            self.session.delete(utilisateur)
            self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            raise ValueError(f"Erreur lors de la suppression : {str(e)}")
    
    # -------------------------------------------------
    # UTILITAIRES
    # -------------------------------------------------
    def email_existe(self, email: str) -> bool:
        """Vérifier si un email existe déjà."""
        return self.obtenir_par_email(email) is not None
    
    def compter_utilisateurs(self) -> int:
        """Compter le nombre total d'utilisateurs."""
        statement = select(Utilisateur)
        return len(self.session.exec(statement).all())
