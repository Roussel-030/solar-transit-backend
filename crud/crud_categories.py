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


categories = CRUDCategories(Categories)

# begin #
# ---write your code here--- #
# end #
