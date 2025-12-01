from app.db.session import get_db
from app.schemas.user import UserCreate

async def create_user(user: UserCreate):
    db = await get_db()
    # Logique pour créer un utilisateur
    await db.users.insert_one(user.dict())
