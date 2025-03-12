from db.base_class import Base
from sqlalchemy import Column, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from sqlalchemy import String, Text, Integer, Float


class ListingImages(Base):
    __tablename__ = 'listing_images'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True, index=True)
    listing_id = Column(Integer, ForeignKey('categories.id'))
    image_url = Column(String(80), nullable=True)

    # default column
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relations
    listing = relationship('Categories', foreign_keys=[listing_id])
