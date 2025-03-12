# begin #
# ---write your code here--- #
# end #

from typing import Optional, List, Any
from sqlalchemy.orm import Session

from crud.base import CRUDBase
from models.categories import Categories
from schemas.categories import CategoriesCreate, CategoriesUpdate


class CRUDCategories(CRUDBase[Categories, CategoriesCreate, CategoriesUpdate]):
    def get_by_id(self, db: Session, *, id: int) -> Optional[Categories]:
        return db.query(Categories).filter(Categories.id == id).first()

    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[Categories]:
        return db.query(Categories).offset(skip).limit(limit).all()

    def get_by_field(self, db: Session, *, field: str, value: Any) -> Optional[Categories]:
        return db.query(Categories).filter(getattr(Categories, field) == value).first()

    def delete(self, db: Session, *, id: int) -> Categories:
        obj = db.query(Categories).filter(Categories.id == id).first()
        db.delete(obj)
        db.commit()
        return obj


categories = CRUDCategories(Categories)

# begin #
# ---write your code here--- #
# end #
