import secrets
from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt

from app.config import settings
from app.db.repositories.utilisateur_repository import UtilisateurRepository
from app.db.models.utilisateur import Utilisateur
from app.schemas.utilisateur import UtilisateurCreate

# Configuration
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    """Service pour gérer l'authentification et l'inscription"""
    
    def __init__(self, db: Session):
        self.db = db
        self.repo = UtilisateurRepository(db)
    
    # ========================================
    # UTILITAIRES MOT DE PASSE
    # ========================================
    
    def hash_password(self, password: str) -> str:
        """Hasher un mot de passe"""
        return pwd_context.hash(password)
    
    def verify_password(self, plain: str, hashed: str) -> bool:
        """Vérifier un mot de passe"""
        return pwd_context.verify(plain, hashed)
    
    # ========================================
    # GÉNÉRATION DE TOKENS
    # ========================================
    
    def generate_verification_token(self) -> str:
        """Générer un token de vérification email (6 chiffres)"""
        return str(secrets.randbelow(900000) + 100000)  # 100000-999999
    
    def create_access_token(self, user_id: int, role: str) -> str:
        """Créer un token JWT d'accès"""
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        to_encode = {
            "sub": str(user_id),
            "role": role,
            "exp": expire
        }
        return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    
    # ========================================
    # INSCRIPTION CLASSIQUE
    # ========================================
    
    def register_user(self, user_data: UtilisateurCreate) -> tuple[Utilisateur, str]:
        """
        Inscrire un nouvel utilisateur (rôle: utilisateur)
        Retourne (utilisateur, code_verification)
        """
        # Vérifier si l'email existe déjà
        if self.repo.email_existe(user_data.email):
            raise ValueError("Cet email est déjà utilisé")
        
        # Générer le code de vérification
        code_verification = self.generate_verification_token()
        
        # Créer l'utilisateur
        new_user = Utilisateur(
            prenom=user_data.prenom,
            nom=user_data.nom,
            email=user_data.email,
            mot_de_passe=self.hash_password(user_data.mot_de_passe),
            role="utilisateur",  # Rôle par défaut
            email_verifie=False,  # Pas encore vérifié
            code_verification=code_verification,
            code_expiration=datetime.utcnow() + timedelta(hours=24)  # Expire dans 24h
        )
        
        created_user = self.repo.creer_utilisateur(new_user)
        return created_user, code_verification
    
    def verify_email(self, email: str, code: str) -> Utilisateur:
        """
        Vérifier l'email avec le code reçu
        """
        user = self.repo.obtenir_par_email(email)
        
        if not user:
            raise ValueError("Utilisateur introuvable")
        
        if user.email_verifie:
            raise ValueError("Email déjà vérifié")
        
        # Vérifier le code
        if user.code_verification != code:
            raise ValueError("Code de vérification incorrect")
        
        # Vérifier l'expiration
        if datetime.utcnow() > user.code_expiration:
            raise ValueError("Code expiré. Demandez un nouveau code")
        
        # Valider l'email
        user.email_verifie = True
        user.code_verification = None
        user.code_expiration = None
        
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def resend_verification_code(self, email: str) -> str:
        """
        Renvoyer un code de vérification
        """
        user = self.repo.obtenir_par_email(email)
        
        if not user:
            raise ValueError("Utilisateur introuvable")
        
        if user.email_verifie:
            raise ValueError("Email déjà vérifié")
        
        # Générer nouveau code
        new_code = self.generate_verification_token()
        user.code_verification = new_code
        user.code_expiration = datetime.utcnow() + timedelta(hours=24)
        
        self.db.commit()
        return new_code
    
    # ========================================
    # FRANCE CONNECT
    # ========================================
    
    def register_or_login_franceconnect(
        self,
        email: str,
        prenom: str,
        nom: str,
        france_connect_id: str
    ) -> Utilisateur:
        """
        Inscription/Connexion via FranceConnect (rôle: membre)
        Si l'utilisateur existe déjà, on le connecte
        Sinon on crée un compte membre
        """
        # Chercher par email
        user = self.repo.obtenir_par_email(email)
        
        if user:
            # L'utilisateur existe, on le met à jour si nécessaire
            if not user.france_connect_id:
                user.france_connect_id = france_connect_id
                # Upgrade vers membre si c'était un utilisateur simple
                if user.role == "utilisateur":
                    user.role = "membre"
                self.db.commit()
                self.db.refresh(user)
            return user
        
        # Créer un nouveau membre via FranceConnect
        new_member = Utilisateur(
            prenom=prenom,
            nom=nom,
            email=email,
            mot_de_passe=self.hash_password(secrets.token_urlsafe(32)),  # Mot de passe aléatoire
            role="membre",  # FranceConnect = membre automatique
            email_verifie=True,  # Email vérifié par FranceConnect
            france_connect_id=france_connect_id
        )
        
        created_member = self.repo.creer_utilisateur(new_member)
        return created_member
    
    # ========================================
    # CONNEXION
    # ========================================
    
    def authenticate(self, email: str, password: str) -> Utilisateur:
        """
        Authentifier un utilisateur
        """
        user = self.repo.obtenir_par_email(email)
        
        if not user:
            raise ValueError("Email ou mot de passe incorrect")
        
        if not self.verify_password(password, user.mot_de_passe):
            raise ValueError("Email ou mot de passe incorrect")
        
        if not user.email_verifie:
            raise ValueError("Veuillez vérifier votre email avant de vous connecter")
        
        return user