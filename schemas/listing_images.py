# begin #
# ---write your code here--- #
# end #

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class ListingImagesBase(BaseModel):
    image_url: Optional[str]
    listing_id: Optional[int]


class ListingImagesCreate(ListingImagesBase):
    image_url: str
    listing_id: int


class ListingImagesUpdate(ListingImagesBase):
    pass


class ListingImagesInDBBase(ListingImagesBase):
    id: Optional[int]
    listing_id: Optional[int]

    class Config:
        orm_mode = True


class ListingImages(ListingImagesInDBBase):
    pass


class ListingImagesInDB(ListingImagesInDBBase):
    pass


class ResponseListingImages(BaseModel):
    count: int
    data: Optional[List[ListingImages]]

# begin #
# ---write your code here--- #
# end #
