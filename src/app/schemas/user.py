from pydantic import BaseModel, EmailStr


### exemple de schema pour un utilisateur
class UserBase(BaseModel):
    email: EmailStr
    full_name: str

class UserCreate(UserBase):
    password: str
