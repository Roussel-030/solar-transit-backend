# begin #
# ---write your code here--- #
# end #

from db.base_class import Base
from sqlalchemy import Column, DateTime, func
from sqlalchemy import String, Integer


class Categories(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True, index=True)
    name = Column(String(80), nullable=False, unique=True)

    # default column
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relations


# begin #
# ---write your code here--- #
# end #
