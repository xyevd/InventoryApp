from sqlalchemy import (
    Column, Integer, ForeignKey, DateTime, CheckConstraint
)
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class StockMovement(Base):
    __tablename__ = "stock_movement"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="RESTRICT"), nullable=False)
    product_id = Column(Integer, ForeignKey("product.id", ondelete="RESTRICT"), nullable=False)
    from_loc = Column(Integer, ForeignKey("location.id", ondelete="RESTRICT"), nullable=True)
    to_loc = Column(Integer, ForeignKey("location.id", ondelete="RESTRICT"), nullable=True)
    quantity = Column(Integer, nullable=False)
    moved_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="stock_movements", passive_deletes=True)
    product = relationship("Product", back_populates="stock_movements", passive_deletes=True)
    from_location = relationship(
        "Location",
        foreign_keys=lambda: [StockMovement.from_loc],
        back_populates="stock_movements_from",
        passive_deletes=True
    )
    to_location = relationship(
        "Location",
        foreign_keys=lambda: [StockMovement.to_loc],
        back_populates="stock_movements_to",
        passive_deletes=True
    )

    __table_args__ = (
        CheckConstraint("quantity > 0", name="check_quantity_positive"),
        CheckConstraint(
            "(from_loc IS NOT NULL AND to_loc IS NOT NULL AND from_loc != to_loc) OR "
            "(from_loc IS NOT NULL AND to_loc IS NULL) OR "
            "(from_loc IS NULL AND to_loc IS NOT NULL)",
            name="check_locations_valid"
        ),
    )