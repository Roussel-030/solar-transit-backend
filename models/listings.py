from db.base_class import Base
from sqlalchemy import Column, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from sqlalchemy import String, Text, Integer, Float


class Listings(Base):
    __tablename__ = 'listings'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True, index=True)
    name = Column(String(80), nullable=False)
    description = Column(Text, nullable=False)
    address = Column(String(80), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float)
    category_id = Column(Integer, ForeignKey('categories.id'))
    created_by = Column(Integer, ForeignKey('users.id'))

    # default column
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relations
    categories = relationship('Categories', foreign_keys=[category_id])
    users = relationship('Users', foreign_keys=[created_by])
