from sqlalchemy import (
    Column,
    String,
    Integer,
    Float,
    DateTime,
    ForeignKey
)

from sqlalchemy.orm import relationship

from database import Base


class Expense(Base):

    __tablename__ = "expenses"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    description = Column(
        String(255),
        nullable=False
    )

    amount = Column(
        Float,
        nullable=False
    )

    category = Column(
        String(100),
        nullable=False
    )

    date = Column(
        DateTime,
        nullable=False
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    type = Column(
        String(50),
        default="expense"
    )

    user = relationship(
        "User",
        backref="expenses"
    )

    def __repr__(self):

        return (
            f"<Expense(description={self.description}, "
            f"amount={self.amount}, "
            f"category={self.category})>"
        )

