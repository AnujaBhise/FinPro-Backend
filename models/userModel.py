from sqlalchemy import Column, String, Integer
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=False)

    email = Column(String(255), nullable=False, unique=True)

    password = Column(String(255), nullable=False)

    def __repr__(self):
        return f"<User(name={self.name}, email={self.email})>"