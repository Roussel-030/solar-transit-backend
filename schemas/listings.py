# begin #
# ---write your code here--- #
# end #

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from .categories import Categories
from .users import Users


class ListingsBase(BaseModel):
    name: Optional[str]
    description: Optional[str]
    address: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float] = None
    category_id: Optional[int]


class ListingsCreate(ListingsBase):
    name: str
    description: str
    address: str
    latitude: float
    category_id: int
    created_by: Optional[int] = None


class ListingsUpdate(ListingsBase):
    pass


class ListingsInDBBase(ListingsBase):
    id: Optional[int]
    category_id: Optional[int]
    created_by: Optional[int]

    class Config:
        orm_mode = True


class Listings(ListingsInDBBase):
    categories: Optional[Categories] = None
    users: Optional[Users] = None


class ListingsInDB(ListingsInDBBase):
    pass


class ResponseListings(BaseModel):
    count: int
    data: Optional[List[Listings]]


# begin #
# ---write your code here--- #
# end #
