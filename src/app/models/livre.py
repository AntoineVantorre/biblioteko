from datetime import datetime
from typing import List, Optional
from pydantic import Field as PydField, BaseModel, HttpUrl
from sqlmodel import SQLModel, Field, Index


class Image(BaseModel):
    id_image: int
    nom_image: str
    format: str
    taille: int = PydField(..., ge=0, description="Taille en ko")


class Livre(SQLModel, table=True):
    id_livre: Optional[int] = Field(default=None, primary_key=True)
    titre: str = Field(..., min_length=1)
    auteur: str = Field(..., min_length=1)
    description: str = Field(default="", max_length=2000)
    lien_contenu: HttpUrl = Field(..., description="Lien GitHub contenant le contenu du livre")
    type: str = Field(..., min_length=1)
    date_ajout: datetime = Field(default_factory=datetime.now)

    __table_args__ = (
        Index("idx_titre", "titre"),
        Index("idx_auteur", "auteur"),
    )