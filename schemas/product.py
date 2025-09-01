from pydantic import BaseModel, Field, constr
from typing import Optional

class ProductCreate(BaseModel):
    name: constr(min_length=3, max_length=50)
    price: int = Field(..., gt=0)

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=50)
    price: Optional[int] = Field(None, gt=0)

class ProductRead(BaseModel):
    id: int
    name: str
    price: int

    class Config:
        from_attributes = True