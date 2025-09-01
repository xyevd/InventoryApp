from enum import Enum
from pydantic import BaseModel, constr, Field
from typing import Optional

class LocationRole(str, Enum):
    store = "Store"
    warehouse = "Warehouse"

class LocationCreate(BaseModel):
    name: constr(min_length=3, max_length=50)
    role: LocationRole

class LocationRead(BaseModel):
    id: int
    name: str
    role: str

class LocationUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=50)
    role: Optional[LocationRole] = None

    class Config:
        from_attributes = True