# begin #
# ---write your code here--- #
# end #

import schemas
import crud
from utils import pick_random_key_value
from fastapi.encoders import jsonable_encoder


def test_create_listings(db):
    listings_data = schemas.ListingsCreate(**{'id': 9, 'name': '7L', 'description': 'pBOoIGQ08ZRe98Y', 'address': 'x8vz9blE', 'latitude': 2.030288501312902, 'category_id': 2, 'created_by': 9})
    listings = crud.listings.create(db=db, obj_in=listings_data)
    data_json = pick_random_key_value(jsonable_encoder(listings_data))
    test_json = jsonable_encoder(listings)
    assert listings.id is not None
    assert test_json[data_json[0]] == data_json[1]


def test_update_listings(db):
    # Create a record first
    listings_data = schemas.ListingsCreate(**{'id': 18, 'name': 'nWoO', 'description': 'aQKo', 'address': 'v', 'latitude': 2.1009769142753774, 'category_id': 17, 'created_by': 18})
    listings = crud.listings.create(db=db, obj_in=listings_data)
    assert listings.id is not None

    # Update the record
    update_data = schemas.ListingsUpdate(**{'id': 19, 'name': 'uG91', 'description': 'QuisQH6gSTTaKbQEyj0C13z8xdjv', 'address': 'F', 'latitude': 4.92434965501576, 'category_id': 11, 'created_by': 4})
    updated_listings = crud.listings.update(db=db, db_obj=listings, obj_in=update_data)
    assert updated_listings.id == listings.id
    assert updated_listings != listings  # Ensure the record was actually updated


def test_get_listings(db):
    # Create a record first
    listings_data = schemas.ListingsCreate(**{'id': 18, 'name': 'qNxjcT', 'description': 'rMliydCfEYTU9mNWVLew9vUNcgqUzzLxzkdebWGZDY4Ep', 'address': 'fRrY', 'latitude': 4.436251955988445, 'category_id': 9, 'created_by': 14})
    listings = crud.listings.create(db=db, obj_in=listings_data)
    assert listings.id is not None

    # Retrieve all records
    records = crud.listings.get_multi(db=db)
    assert len(records) > 0
    assert any(record.id == listings.id for record in records)


def test_get_by_id_listings(db):
    # Create a record first
    listings_data = schemas.ListingsCreate(**{'id': 3, 'name': '', 'description': 'ZEWTNQsdCDvlKC9ahF1XUiJgWFRkFmqTxKtPeG3nsOSi5k5k0arYnr5kqYHtM1PUa4sym1axWJr', 'address': 'X', 'latitude': 2.406184880136778, 'category_id': 18, 'created_by': 17})
    listings = crud.listings.create(db=db, obj_in=listings_data)
    assert listings.id is not None

    # Retrieve the record by ID
    retrieved_listings = crud.listings.get(db=db, id=listings.id)
    assert retrieved_listings is not None
    assert retrieved_listings.id == listings.id
    assert retrieved_listings == listings


def test_delete_listings(db):
    # Create a record first
    listings_data = schemas.ListingsCreate(**{'id': 17, 'name': 'ER', 'description': 'oIwPyWeXQ6ZqAr', 'address': 'gOazES55y', 'latitude': 4.0618073361174165, 'category_id': 9, 'created_by': 5})
    listings = crud.listings.create(db=db, obj_in=listings_data)
    assert listings.id is not None

    # Delete the record
    deleted_listings = crud.listings.remove(db=db, id=listings.id)
    assert deleted_listings is not None
    assert deleted_listings.id == listings.id

    # Ensure the record is no longer retrievable
    retrieved_listings = crud.listings.get(db=db, id=listings.id)
    assert retrieved_listings is None

# begin #
# ---write your code here--- #
# end #
