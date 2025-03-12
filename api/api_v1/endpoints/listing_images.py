import os
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

import models
import schemas
import crud
from api import deps

router = APIRouter()

# Dossier pour stocker les images
IMAGE_DIR = "images"


@router.get('/', response_model=schemas.ResponseListingImages)
def read_listing_images(
        db: Session = Depends(deps.get_db),
        current_user: models.Users = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve listing_imagess.
    """
    listing_imagess = crud.listing_images.get_multi(db=db)
    count = crud.listing_images.get_count(db=db)
    response = schemas.ResponseListingImages(**{'count': count, 'data': jsonable_encoder(listing_imagess)})
    return response


@router.post('/', response_model=schemas.ListingImages)
def create_listing_images(
        *,
        db: Session = Depends(deps.get_db),
        listing_images_in: schemas.ListingImagesCreate,
        current_user: models.Users = Depends(deps.get_current_user),
) -> Any:
    """
    Create new listing_images.
    """
    listing_images = crud.listing_images.create(db=db, obj_in=listing_images_in)
    return listing_images


@router.put('/', response_model=schemas.ListingImages)
def update_listing_images(
        *,
        db: Session = Depends(deps.get_db),
        listing_images_id: int,
        listing_images_in: schemas.ListingImagesUpdate,
        current_user: models.Users = Depends(deps.get_current_user),
) -> Any:
    """
    Update an listing_images.
    """
    listing_images = crud.listing_images.get(db=db, id=listing_images_id)
    if not listing_images:
        raise HTTPException(status_code=404, detail='ListingImages not found')

    if listing_images.created_by != current_user.id:
        raise HTTPException(status_code=404, detail='Not enaught permission')

    listing_images = crud.listing_images.update(db=db, db_obj=listing_images, obj_in=listing_images_in)
    return listing_images


@router.get('/by_id/', response_model=schemas.ListingImages)
def read_listing_images(
        *,
        db: Session = Depends(deps.get_db),
        listing_images_id: int,
        current_user: models.Users = Depends(deps.get_current_user),
) -> Any:
    """
    Get listing_images by ID.
    """
    listing_images = crud.listing_images.get(db=db, id=listing_images_id)
    if not listing_images:
        raise HTTPException(status_code=404, detail='ListingImages not found')
    return listing_images


@router.delete('/', response_model=schemas.ListingImages)
def delete_listing_images(
        *,
        db: Session = Depends(deps.get_db),
        listing_images_id: int,
        current_user: models.Users = Depends(deps.get_current_user),
) -> Any:
    """
    Delete an listing_images.
    """
    listing_images = crud.listing_images.get(db=db, id=listing_images_id)
    if not listing_images:
        raise HTTPException(status_code=404, detail='ListingImages not found')

    if listing_images.created_by != current_user.id:
        raise HTTPException(status_code=404, detail='Not enaught permission')

    listing_images = crud.listing_images.remove(db=db, id=listing_images_id)
    return listing_images


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

    return file_path
