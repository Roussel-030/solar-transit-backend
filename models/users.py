from db.base_class import Base
from sqlalchemy import Column, DateTime, func, String, Boolean, Integer, Enum
from enum import Enum as PyEnum


# Define the Enum for roles
class UserRole(PyEnum):
    ADMIN = "admin"
    USER = "user"


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True, index=True)
    username = Column(String(80), nullable=False, unique=True, index=True)
    password = Column(String(80), nullable=False)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.USER)  # Use Enum for role

    # default column
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
