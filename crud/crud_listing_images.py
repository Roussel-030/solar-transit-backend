from typing import Optional, List, Any
from sqlalchemy.orm import Session

from crud.base import CRUDBase
from models.listing_images import ListingImages
from schemas.listing_images import ListingImagesCreate, ListingImagesUpdate


class CRUDListingImages(CRUDBase[ListingImages, ListingImagesCreate, ListingImagesUpdate]):
    def get_by_id(self, db: Session, *, id: int) -> Optional[ListingImages]:
        return db.query(ListingImages).filter(ListingImages.id == id).first()

    def get_by_listing(self, db: Session, *, listing_id: int) -> Optional[ListingImages]:
        return db.query(ListingImages).filter(ListingImages.listing_id == listing_id).all()


listing_images = CRUDListingImages(ListingImages)
