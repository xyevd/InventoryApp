from sqlalchemy import Column, Integer, String, CheckConstraint
from sqlalchemy.orm import relationship
from database import Base
from .stockmovement import StockMovement

class Location(Base):
    __tablename__ = "location"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    role = Column(String, nullable=False)

    stock_movements_from = relationship(
        "StockMovement",
        back_populates="from_location",
        foreign_keys=lambda: [StockMovement.from_loc],
        passive_deletes=True
    )
    stock_movements_to = relationship(
        "StockMovement",
        back_populates="to_location",
        foreign_keys=lambda: [StockMovement.to_loc],
        passive_deletes=True
    )


__table_args__ = (
        CheckConstraint("role IN ('Warehouse', 'Store')", name="check_loc_role"),
    )