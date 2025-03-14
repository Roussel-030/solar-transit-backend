from typing import Optional

from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str
    role: str


class TokenPayload(BaseModel):
    id: Optional[int] = None
    username: Optional[str]
