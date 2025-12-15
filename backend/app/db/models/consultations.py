from datetime import datetime
from pydantic import EmailStr
from sqlmodel import ForeignKey, SQLModel, Field, Index
from typing import List, Optional


class Utilisateur(SQLModel, table=True):
    __tablename__ = "consultations"

    id: int = Field(primary_key=True)
    user_id: int = Field(ForeignKey("users.id"))
    book_id: int = Field(ForeignKey("books.id"))
    consulted_at: datetime = Field(default=datetime.now)