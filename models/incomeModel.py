from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Income(Base):
    __tablename__ = "incomes"

    id = Column(Integer, primary_key=True, index=True)

    description = Column(String(255), nullable=False)

    amount = Column(Float, nullable=False)

    category = Column(String(100), nullable=False)

    date = Column(DateTime, nullable=False)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    type = Column(String(50), default="income")

    user = relationship("User", backref="incomes")

    def __repr__(self):
        return f"<Income(description={self.description}, amount={self.amount}, category={self.category})>"
