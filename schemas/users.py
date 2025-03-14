from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr


class UsersBase(BaseModel):
    username: Optional[EmailStr]
    password: Optional[str]
    role: Optional[str]


class UsersCreate(UsersBase):
    username: EmailStr
    password: str
    role: str = "user"


class UsersUpdate(UsersBase):
    pass


class UsersInDBBase(UsersBase):
    id: Optional[int]
    created_at: Optional[datetime]

    class Config:
        orm_mode = True


class Users(UsersInDBBase):
    pass


class UsersInDB(UsersInDBBase):
    pass


class ResponseUsers(BaseModel):
    count: int
    data: Optional[List[Users]]
