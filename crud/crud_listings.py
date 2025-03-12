from typing import Optional, List, Any
from sqlalchemy.orm import Session

from crud.base import CRUDBase
from models.listings import Listings
from schemas.listings import ListingsCreate, ListingsUpdate


class CRUDListings(CRUDBase[Listings, ListingsCreate, ListingsUpdate]):
    def get_by_id(self, db: Session, *, id: int) -> Optional[Listings]:
        return db.query(Listings).filter(Listings.id == id).first()

    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[Listings]:
        return db.query(Listings).offset(skip).limit(limit).all()

    def get_by_field(self, db: Session, *, field: str, value: Any) -> Optional[Listings]:
        return db.query(Listings).filter(getattr(Listings, field) == value).first()

    def delete(self, db: Session, *, id: int) -> Listings:
        obj = db.query(Listings).filter(Listings.id == id).first()
        db.delete(obj)
        db.commit()
        return obj


listings = CRUDListings(Listings)
