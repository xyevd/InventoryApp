from enum import Enum
from pydantic import BaseModel, constr

class UserRole(str, Enum):
    user = "user"
    admin = "admin"

class UserCreate(BaseModel):
    username: constr(min_length=3, max_length=50)
    password: constr(min_length=6, max_length=255)
    role: UserRole

class UserRead(BaseModel):
    id: int
    username: str
    role: str

    class Config:
        from_attributes = True  # enable return of orm obj