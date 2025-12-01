from motor.motor_asyncio import AsyncIOMotorClient
from app.config import MONGODB_URL

client = AsyncIOMotorClient(MONGODB_URL)
db = client.ma_base_de_donnees

async def get_db():
    return db
