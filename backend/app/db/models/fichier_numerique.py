from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Column
from enum import Enum

class Domaine(Enum):
    LITTERATURE = "litterature"
    SCIENCE = "science"
    HISTOIRE = "histoire"
    ART = "art"
    TECHNOLOGIE = "technologie"
    FICTION = "fiction"
    NON_FICTION = "non_fiction"
    EDUCATIF = "educatif"
    REFERENCE = "reference"
    AUTRE = "autre"

class Categorie(Enum):
    LIVRE = "livre"
    AUDIOBOOK = "audiobook"
    VIDEO = "video"
    IMAGE = "image"
    DOCUMENT = "document"
    AUTRE = "autre"


class FichierNumerique(SQLModel, table=True):
    __tablename__ = "fichiers_numeriques"

    id_fichier: Optional[int] = Field(default=None, primary_key=True)

    # Nom lisible par l’utilisateur (ex : "Les Misérables - Tome 1")
    titre: str = Field(index=True, min_length=1, max_length=255)

    # Le nom ou chemin du fichier sur GitHub (ex : "/ebooks/les_miserables_t1.pdf")
    chemin_github: str = Field(unique=True, min_length=1, max_length=500)

    # Type du fichier : pdf, epub, audio, video, etc.
    type_fichier: str = Field(regex=r"^(pdf|epub|audio|video|image|autre)$", max_length=20)

    # Date d’ajout
    date_ajout: datetime = Field(default_factory=datetime.utcnow)

    categorie: Categorie

    domaine: Domaine

    class Config:
        arbitrary_types_allowed = True