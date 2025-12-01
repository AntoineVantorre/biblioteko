from fastapi import APIRouter, Depends
from app.db.models.user import create_user
from app.schemas.user import UserCreate

router = APIRouter()

@router.post("/register")
async def register(user: UserCreate):
    await create_user(user)
    return {"message": "Utilisateur créé"}
