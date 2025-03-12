# begin #
# ---write your code here--- #
# end #

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class CategoriesBase(BaseModel):
    name: Optional[str]


class CategoriesCreate(CategoriesBase):
    name: str


class CategoriesUpdate(CategoriesBase):
    pass


class CategoriesInDBBase(CategoriesBase):
    id: Optional[int]

    class Config:
        orm_mode = True


class Categories(CategoriesInDBBase):
    pass


class CategoriesInDB(CategoriesInDBBase):
    pass


class ResponseCategories(BaseModel):
    count: int
    data: Optional[List[Categories]]


# begin #
# ---write your code here--- #
# end #
