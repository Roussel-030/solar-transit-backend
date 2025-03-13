from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

import models
import schemas
import crud
from api import deps

router = APIRouter()


@router.get('/', response_model=schemas.ResponseListings)
def read_listings(
        db: Session = Depends(deps.get_db),
        offset: int = 0,
        limit: int = 20,
        current_user: models.Users = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve listingss.
    """
    listings = crud.listings.get_multi(db=db, skip=offset, limit=limit)
    count = crud.listings.get_count(db=db)
    for listing in listings:
        images = crud.listing_images.get_by_listing(db=db, listing_id=listing.id)
        listing.images = jsonable_encoder(images)
    response = schemas.ResponseListings(**{'count': count, 'data': jsonable_encoder(listings)})
    return response


@router.get('/search', response_model=schemas.ResponseListings)
def search_listings(
        db: Session = Depends(deps.get_db),
        *,
        name: str = "",
        category_id: int = 0,
        current_user: models.Users = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve listingss.
    """

    if name or category_id:
        listings = crud.listings.search(db=db, name=name, category_id=category_id)
        count = crud.listings.search_count(db=db, name=name, category_id=category_id)
        response = schemas.ResponseListings(**{'count': count, 'data': jsonable_encoder(listings)})
    else:
        listings = crud.listings.get_multi(db=db)
        count = crud.listings.get_count(db=db)
        response = schemas.ResponseListings(**{'count': count, 'data': jsonable_encoder(listings)})
    return response

@router.post('/', response_model=schemas.Listings)
def create_listings(
        *,
        db: Session = Depends(deps.get_db),
        listings_in: schemas.ListingsCreate,
        current_user: models.Users = Depends(deps.get_current_user),
) -> Any:
    """
    Create new listings.
    """
    listings_in.created_by = current_user.id
    listings = crud.listings.create(db=db, obj_in=listings_in)
    return listings


@router.put('/', response_model=schemas.Listings)
def update_listings(
        *,
        db: Session = Depends(deps.get_db),
        listings_id: int,
        listings_in: schemas.ListingsUpdate,
        current_user: models.Users = Depends(deps.get_current_user),
) -> Any:
    """
    Update an listings.
    """
    listings = crud.listings.get(db=db, id=listings_id)
    if not listings:
        raise HTTPException(status_code=404, detail='Listings not found')

    if listings.created_by != current_user.id:
        raise HTTPException(status_code=404, detail='Not enaught permission')

    listings = crud.listings.update(db=db, db_obj=listings, obj_in=listings_in)
    return listings


@router.get('/by_id/', response_model=schemas.Listings)
def read_listings(
        *,
        db: Session = Depends(deps.get_db),
        listings_id: int,
        current_user: models.Users = Depends(deps.get_current_user),
) -> Any:
    """
    Get listings by ID.
    """
    listings = crud.listings.get(db=db, id=listings_id)
    images = crud.listing_images.get_by_listing(db=db, listing_id=listings.id)
    listings.images = jsonable_encoder(images)
    if not listings:
        raise HTTPException(status_code=404, detail='Listings not found')
    return listings


@router.delete('/', response_model=schemas.Listings)
def delete_listings(
        *,
        db: Session = Depends(deps.get_db),
        listings_id: int,
        current_user: models.Users = Depends(deps.get_current_user),
) -> Any:
    """
    Delete an listings.
    """
    listings = crud.listings.get(db=db, id=listings_id)
    if not listings:
        raise HTTPException(status_code=404, detail='Listings not found')

    if listings.created_by != current_user.id:
        raise HTTPException(status_code=404, detail='Not enaught permission')

    listings = crud.listings.remove(db=db, id=listings_id)
    return listings
