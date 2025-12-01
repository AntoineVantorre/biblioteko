from fastapi import Depends
from app.db.session import get_db

async def get_current_db(db=Depends(get_db)):
    return db
