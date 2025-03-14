from typing import Optional, List, Any, Union, Dict
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
            role=obj_in.role,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
            self, db: Session, *, db_obj: Users, obj_in: Union[UsersUpdate, Dict[str, Any]]
    ) -> Users:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if "password" in update_data:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["password"] = hashed_password
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def is_admin(self, user: Users):
        return user.role == UserRole.ADMIN


users = CRUDUsers(Users)
