from typing import Optional, List, Any
from sqlalchemy.orm import Session

from core.security import verify_password, get_password_hash
from crud.base import CRUDBase
from models.users import Users, UserRole
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

    def create(self, db: Session, *, obj_in: UsersCreate) -> Users:
        db_obj = Users(
            username=obj_in.username,
            password=get_password_hash(obj_in.password),
            role=obj_in.id_role,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def is_admin(self, user: Users):
        return user.role == UserRole.ADMIN


users = CRUDUsers(Users)
