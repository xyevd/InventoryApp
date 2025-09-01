from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)

    stock_movements = relationship(
        "StockMovement",
        back_populates="product",
        passive_deletes=True
    )
