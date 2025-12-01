from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import os
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional

router = APIRouter()

# Use absolute token URL to match router prefix in main.py
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

# MongoDB client setup (reads MONGO_URI and MONGO_DB from env)
MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongodb:27017")
MONGO_DB = os.getenv("MONGO_DB", "biblioteko")

_motor_client = AsyncIOMotorClient(MONGO_URI)
_db = _motor_client[MONGO_DB]
_users_coll = _db["users"]

def fake_hash_password(password: str):
    return "fakehashed" + password

async def get_user(username: str) -> Optional[dict]:
    user = await _users_coll.find_one({"username": username})
    if not user:
        return None
    # convert ObjectId to str and remove internal fields if needed
    user["_id"] = str(user["_id"])
    return user

@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await get_user(form_data.username)
    if not user or user.get("hashed_password") != fake_hash_password(form_data.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return {"access_token": user["username"], "token_type": "bearer"}

@router.get("/users/me")
async def read_users_me(token: str = Depends(oauth2_scheme)):
    user = await get_user(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    # Remove sensitive fields before returning
    user.pop("hashed_password", None)
    return user