from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, model_validator

class StockMovementCreate(BaseModel):
    user_id: int
    product_id: int
    from_loc: Optional[int] = None
    to_loc: Optional[int] = None
    quantity: int = Field(..., gt=0)
    @model_validator(mode="after")

    def _validate_route(self):
        if self.from_loc is None and self.to_loc is None:
            raise ValueError("At least one from_loc/to_loc is required.")
        if self.from_loc is not None and self.to_loc is not None and self.from_loc == self.to_loc:
            raise ValueError("from_loc and to_loc have to be different.")
        return self


class StockMovementRead(BaseModel):
    id: int
    user_id: int
    product_id: int
    from_loc: Optional[int]
    to_loc: Optional[int]
    quantity: int
    moved_at: datetime

    class Config:
        from_attributes = True