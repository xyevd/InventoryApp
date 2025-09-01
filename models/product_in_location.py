from sqlalchemy import Column, Integer, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from database import Base

class ProductInLocation(Base):
    __tablename__ = "product_in_location"

    product_id = Column(Integer, ForeignKey("product.id", ondelete="RESTRICT"), primary_key=True)
    location_id = Column(Integer, ForeignKey("location.id", ondelete="RESTRICT"), primary_key=True)
    quantity = Column(Integer, nullable=False)

    product = relationship("Product")
    location = relationship("Location")

    __table_args__ = (
        CheckConstraint("quantity >= 0", name="check_quantity_positive_loc"),
    )
