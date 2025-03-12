from typing import List, Optional
from pydantic import BaseModel


class UsersBase(BaseModel):
    username: Optional[str]
    password: Optional[str]
    role: Optional[str]


class UsersCreate(UsersBase):
    username: str
    password: str
    role: str = "user"


class UsersUpdate(UsersBase):
    pass


class UsersInDBBase(UsersBase):
    id: Optional[int]

    class Config:
        orm_mode = True


class Users(UsersInDBBase):
    pass


class UsersInDB(UsersInDBBase):
    pass


class ResponseUsers(BaseModel):
    count: int
    data: Optional[List[Users]]
