from typing import Optional, List, Any

from sqlalchemy import and_, func
from sqlalchemy.orm import Session

from crud.base import CRUDBase
from models.listings import Listings
from schemas.listings import ListingsCreate, ListingsUpdate


class CRUDListings(CRUDBase[Listings, ListingsCreate, ListingsUpdate]):
    def search(
            self,
            db: Session,
            name: str = "",
            category_id: int = 0,
            user_id: int = 0,
            current_user_id: int = None
    ) -> List[Listings]:
        filter_ = []
        if name != "":
            filter_.append(func.lower(Listings.name).like(f"%{name.lower()}%"))
        if category_id != 0:
            filter_.append(Listings.category_id == category_id)
        if user_id != 0:
            filter_.append(Listings.created_by == user_id)
        if current_user_id:
            filter_.append(Listings.created_by == current_user_id)

        query = (
            db.query(self.model)
            .filter(and_(*filter_))
        )

        result = query.all()
        return result

    def search_count(
            self,
            db: Session,
            name: str = None,
            category_id: int = None,
            user_id: int = 0,
            current_user_id: int = None
    ) -> List[Listings]:
        filter_ = []
        if name:
            filter_.append(func.lower(Listings.name).like(f"%{name.lower()}%"))
        if category_id:
            filter_.append(Listings.category_id == category_id)
        if user_id != 0:
            filter_.append(Listings.created_by == user_id)
        if current_user_id:
            filter_.append(Listings.created_by == current_user_id)

        query = (
            db.query(self.model)
            .filter(and_(*filter_))
        )

        result = query.count()
        return result


listings = CRUDListings(Listings)
