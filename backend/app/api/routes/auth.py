from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
import httpx

from app.db.session import get_db
from app.config import settings
from app.services.auth_service import AuthService
from app.services.email_service import email_service
from app.schemas.utilisateur import UtilisateurCreate, UtilisateurRead
from app.db.repositories.utilisateur_repository import UtilisateurRepository

router = APIRouter(prefix="/auth", tags=["Authentication"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


# ============================================
# SCHÉMAS PYDANTIC
# ============================================

class RegisterRequest(BaseModel):
    prenom: str
    nom: str
    email: EmailStr
    mot_de_passe: str


class VerifyEmailRequest(BaseModel):
    email: EmailStr
    code: str


class ResendCodeRequest(BaseModel):
    email: EmailStr


class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: UtilisateurRead


# ============================================
# INSCRIPTION CLASSIQUE
# ============================================

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
    data: RegisterRequest,
    db: Session = Depends(get_db)
):
    """
    Inscription d'un nouvel utilisateur (rôle: utilisateur)
    Un code de vérification est envoyé par email
    """
    auth_service = AuthService(db)
    
    try:
        # Créer l'utilisateur
        user_create = UtilisateurCreate(
            prenom=data.prenom,
            nom=data.nom,
            email=data.email,
            mot_de_passe=data.mot_de_passe,
            role="utilisateur"
        )
        
        user, code = auth_service.register_user(user_create)
        
        # Envoyer le code par email
        email_sent = email_service.send_verification_code(
            to_email=user.email,
            prenom=user.prenom,
            code=code
        )
        
        if not email_sent:
            # Si l'email n'a pas pu être envoyé, afficher le code en dev
            if settings.DEBUG:
                return {
                    "message": "Utilisateur créé. ATTENTION: Email non envoyé (mode dev)",
                    "code_debug": code,  # SEULEMENT EN DEV !
                    "email": user.email
                }
        
        return {
            "message": f"Compte créé avec succès ! Un code de vérification a été envoyé à {user.email}",
            "email": user.email
        }
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/verify-email")
async def verify_email(
    data: VerifyEmailRequest,
    db: Session = Depends(get_db)
):
    """
    Vérifier l'email avec le code reçu
    """
    auth_service = AuthService(db)
    
    try:
        user = auth_service.verify_email(data.email, data.code)
        
        # Envoyer email de bienvenue
        email_service.send_welcome_email(user.email, user.prenom)
        
        # Créer le token JWT
        token = auth_service.create_access_token(user.id_utilisateur, user.role)
        
        return {
            "message": "Email vérifié avec succès ! Vous pouvez maintenant vous connecter.",
            "access_token": token,
            "token_type": "bearer",
            "user": UtilisateurRead.from_orm(user)
        }
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/resend-code")
async def resend_verification_code(
    data: ResendCodeRequest,
    db: Session = Depends(get_db)
):
    """
    Renvoyer un code de vérification
    """
    auth_service = AuthService(db)
    
    try:
        code = auth_service.resend_verification_code(data.email)
        
        # Récupérer l'utilisateur pour le prénom
        repo = UtilisateurRepository(db)
        user = repo.obtenir_par_email(data.email)
        
        # Renvoyer l'email
        email_service.send_verification_code(user.email, user.prenom, code)
        
        return {
            "message": f"Un nouveau code a été envoyé à {data.email}"
        }
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


# ============================================
# CONNEXION
# ============================================

@router.post("/login", response_model=LoginResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Connexion avec email et mot de passe
    """
    auth_service = AuthService(db)
    
    try:
        user = auth_service.authenticate(form_data.username, form_data.password)
        
        # Mettre à jour la dernière connexion
        user.derniere_connexion = datetime.utcnow()
        db.commit()
        
        # Créer le token
        token = auth_service.create_access_token(user.id_utilisateur, user.role)
        
        return LoginResponse(
            access_token=token,
            token_type="bearer",
            user=UtilisateurRead.from_orm(user)
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"}
        )


# ============================================
# FRANCE CONNECT
# ============================================

@router.get("/franceconnect/login")
async def franceconnect_login():
    """
    Initier la connexion FranceConnect
    Redirige vers FranceConnect pour l'authentification
    """
    if not settings.FRANCE_CONNECT_CLIENT_ID:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="FranceConnect n'est pas configuré"
        )
    
    # Construire l'URL d'autorisation FranceConnect
    auth_url = (
        f"{settings.FRANCE_CONNECT_AUTHORIZE_URL}"
        f"?client_id={settings.FRANCE_CONNECT_CLIENT_ID}"
        f"&redirect_uri={settings.FRANCE_CONNECT_REDIRECT_URI}"
        f"&response_type=code"
        f"&scope=openid email given_name family_name"
        f"&state=random_state_string"  # À sécuriser en production
    )
    
    return {"redirect_url": auth_url}


@router.get("/franceconnect/callback")
async def franceconnect_callback(
    code: str,
    db: Session = Depends(get_db)
):
    """
    Callback FranceConnect après authentification
    Crée un compte membre ou connecte l'utilisateur existant
    """
    auth_service = AuthService(db)
    
    try:
        # 1. Échanger le code contre un access_token
        async with httpx.AsyncClient() as client:
            token_response = await client.post(
                settings.FRANCE_CONNECT_TOKEN_URL,
                data={
                    "grant_type": "authorization_code",
                    "code": code,
                    "client_id": settings.FRANCE_CONNECT_CLIENT_ID,
                    "client_secret": settings.FRANCE_CONNECT_CLIENT_SECRET,
                    "redirect_uri": settings.FRANCE_CONNECT_REDIRECT_URI
                }
            )
            
            if token_response.status_code != 200:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Erreur lors de l'échange du code FranceConnect"
                )
            
            tokens = token_response.json()
            access_token = tokens.get("access_token")
            
            # 2. Récupérer les infos utilisateur
            userinfo_response = await client.get(
                settings.FRANCE_CONNECT_USERINFO_URL,
                headers={"Authorization": f"Bearer {access_token}"}
            )
            
            if userinfo_response.status_code != 200:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Erreur lors de la récupération des infos utilisateur"
                )
            
            user_info = userinfo_response.json()
        
        # 3. Créer ou connecter l'utilisateur (rôle: membre)
        user = auth_service.register_or_login_franceconnect(
            email=user_info.get("email"),
            prenom=user_info.get("given_name"),
            nom=user_info.get("family_name"),
            france_connect_id=user_info.get("sub")  # ID unique FranceConnect
        )
        
        # 4. Créer le token JWT
        token = auth_service.create_access_token(user.id_utilisateur, user.role)
        
        # 5. Rediriger vers le frontend avec le token
        redirect_url = f"{settings.FRONTEND_URL}/auth/callback?token={token}"
        
        return {
            "redirect_url": redirect_url,
            "access_token": token,
            "user": UtilisateurRead.from_orm(user)
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur FranceConnect: {str(e)}"
        )


# ============================================
# UTILITAIRES
# ============================================

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """Récupère l'utilisateur depuis le token JWT"""
    from jose import jwt, JWTError
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Impossible de valider les credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    repo = UtilisateurRepository(db)
    user = repo.obtenir_par_id(int(user_id))
    
    if user is None:
        raise credentials_exception
    
    return user


@router.get("/me", response_model=UtilisateurRead)
async def get_me(current_user = Depends(get_current_user)):
    """Récupère les infos de l'utilisateur connecté"""
    return current_user


@router.post("/logout")
async def logout():
    """Déconnexion (suppression du token côté client)"""
    return {"message": "Déconnexion réussie"}