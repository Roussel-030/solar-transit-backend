from typing import Optional, List, Any
from sqlalchemy.orm import Session

from core.security import verify_password
from crud.base import CRUDBase
from models.users import Users
from schemas.users import UsersCreate, UsersUpdate


class CRUDUsers(CRUDBase[Users, UsersCreate, UsersUpdate]):
    def get_by_username(self, db: Session, *, username: str) -> Optional[Users]:
        return db.query(Users).filter(Users.username == username).first()

    def authenticate(self, db: Session, *, username: str, password: str) -> Optional[Users]:
        user = self.get_by_username(db, username=username)
        if not user:
            return None
        if not verify_password(password, user.password):
            return None
        return user


users = CRUDUsers(Users)
