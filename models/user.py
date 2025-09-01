from sqlalchemy import Column, Integer, String, CheckConstraint
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False)

    stock_movements = relationship(
        "StockMovement",
        back_populates="user",
        passive_deletes=True
    )

    __table_args__ = (
        CheckConstraint("role IN ('Admin', 'User')", name="check_user_role"),
    )
