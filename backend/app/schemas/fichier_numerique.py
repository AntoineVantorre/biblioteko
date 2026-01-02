from datetime import datetime
from typing import Optional
from enum import Enum
from pydantic import BaseModel

class Domaine(str, Enum):
    litterature = "litterature"
    science = "science"
    histoire = "histoire"
    art = "art"
    technologie = "technologie"
    fiction = "fiction"
    non_fiction = "non_fiction"
    educatif = "educatif"
    reference = "reference"
    autre = "autre"

class Categorie(str, Enum):
    livre = "livre"
    audiobook = "audiobook"
    video = "video"
    image = "image"
    document = "document"
    autre = "autre"

class Etat(str, Enum):
    disponible = "disponible"
    indisponible = "indisponible"
    a_verifier = "a_verifier"

# ------------------------------
# Base
# ------------------------------
class FichierNumeriqueBase(BaseModel):
    titre: Optional[str] = None
    chemin_github: Optional[str] = None
    type_fichier: Optional[str] = None
    categorie: Optional[Categorie] = None
    domaine: Optional[Domaine] = None
    etat: Optional[Etat] = None

# ------------------------------
# Pour la création
# ------------------------------
class FichierNumeriqueCreate(BaseModel):
    titre: str
    chemin_github: str
    type_fichier: str
    categorie: Categorie
    domaine: Domaine
    # Pas besoin de etat ici, il sera mis à A_VERIFIER automatiquement

# ------------------------------
# Pour la modification
# ------------------------------
class FichierNumeriqueUpdate(BaseModel):
    titre: Optional[str] = None
    chemin_github: Optional[str] = None
    type_fichier: Optional[str] = None
    categorie: Optional[Categorie] = None
    domaine: Optional[Domaine] = None
    etat: Optional[Etat] = None

# ------------------------------
# Pour la lecture (retour API)
# ------------------------------
class FichierNumeriqueRead(BaseModel):
    id_fichier: int
    titre: str
    chemin_github: str
    type_fichier: str
    categorie: Categorie
    domaine: Domaine
    etat: Etat
    date_ajout: datetime
    
    class Config:
        from_attributes = True  # Permet la conversion depuis SQLModel

# ------------------------------
# Pour la recherche flexible
# ------------------------------
class FichierNumeriqueSearch(BaseModel):
    titre: Optional[str] = None
    categorie: Optional[Categorie] = None
    domaine: Optional[Domaine] = None
    etat: Optional[Etat] = None