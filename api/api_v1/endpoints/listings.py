import os
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from starlette.responses import FileResponse

import models
import schemas
import crud
from api import deps

router = APIRouter()

IMAGE_DIR = "images"


@router.get('/', response_model=schemas.ResponseListings)
def read_listings(
        db: Session = Depends(deps.get_db),
        offset: int = 0,
        limit: int = 20,
        user_id: int = None,
        current_user: models.Users = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve listingss.
    """
    if crud.users.is_admin(current_user):
        filter_ = []
        if user_id:
            filter_.append(models.Listings.created_by == user_id)
    else:
        filter_ = [models.Listings.created_by == current_user.id]
    listings = crud.listings.get_multi(db=db, skip=offset, limit=limit, filter_=filter_)
    count = crud.listings.get_count(db=db, filter_=filter_)
    response = schemas.ResponseListings(**{'count': count, 'data': jsonable_encoder(listings)})
    return response


@router.get('/search', response_model=schemas.ResponseListings)
def search_listings(
        db: Session = Depends(deps.get_db),
        *,
        name: str = "",
        category_id: int = 0,
        user_id: int = 0,
        current_user: models.Users = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve listingss.
    """
    if crud.users.is_admin(current_user):
        listings = crud.listings.search(db=db, name=name, category_id=category_id, user_id=user_id)
        count = crud.listings.search_count(db=db, name=name, category_id=category_id, user_id=user_id)
    else:
        listings = crud.listings.search(db=db, name=name, category_id=category_id, user_id=user_id,
                                        current_user_id=current_user.id)
        count = crud.listings.search_count(db=db, name=name, category_id=category_id, user_id=user_id,
                                           current_user_id=current_user.id)
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

    if listings.created_by != current_user.id and not crud.users.is_admin(current_user):
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
    if not listings:
        raise HTTPException(status_code=404, detail='Listings not found')
    return listings


@router.delete('/', )
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

    if listings.created_by != current_user.id and not crud.users.is_admin(current_user):
        raise HTTPException(status_code=404, detail='Not enaught permission')

    listings = crud.listings.remove(db=db, id=listings_id)
    return "deleted"


# Endpoint pour télécharger une image
@router.post("/upload-image/")
async def upload_image(file: UploadFile = File(...)):
    # Vérifie si le fichier est une image
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Le fichier doit être une image.")

    # Génère un nom de fichier unique
    file_name = f"{os.urandom(16).hex()}_{file.filename}"
    file_path = os.path.join(IMAGE_DIR, file_name)

    # Sauvegarde le fichier
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    return file_name


@router.get("/image/")
def get_file(name_file: str):
    path = os.getcwd() + "/images/" + name_file
    if os.path.exists(path):
        return FileResponse(path=path)
