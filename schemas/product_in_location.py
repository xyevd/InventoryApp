from pydantic import BaseModel, Field
from typing import Optional

class ProductInLocationCreate(BaseModel):
    product_id: int
    location_id: int
    quantity: int = Field(..., ge=0) # quantity >= 0

class ProductInLocationUpdate(BaseModel):
    quantity: Optional[int] = Field(None, ge=0)

class ProductInLocationRead(BaseModel):
    product_id: int
    location_id: int
    quantity: int

    class Config:
        from_attributes = True