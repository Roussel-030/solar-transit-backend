# begin #
# ---write your code here--- #
# end #

import schemas
import crud
from utils import pick_random_key_value
from fastapi.encoders import jsonable_encoder


def test_create_categories(db):
    categories_data = schemas.CategoriesCreate(**{'id': 20, 'name': '4WYX'})
    categories = crud.categories.create(db=db, obj_in=categories_data)
    data_json = pick_random_key_value(jsonable_encoder(categories_data))
    test_json = jsonable_encoder(categories)
    assert categories.id is not None
    assert test_json[data_json[0]] == data_json[1]


def test_update_categories(db):
    # Create a record first
    categories_data = schemas.CategoriesCreate(**{'id': 7, 'name': 'TBLp4'})
    categories = crud.categories.create(db=db, obj_in=categories_data)
    assert categories.id is not None

    # Update the record
    update_data = schemas.CategoriesUpdate(**{'id': 1, 'name': '3kAtudjD'})
    updated_categories = crud.categories.update(db=db, db_obj=categories, obj_in=update_data)
    assert updated_categories.id == categories.id
    assert updated_categories != categories  # Ensure the record was actually updated


def test_get_categories(db):
    # Create a record first
    categories_data = schemas.CategoriesCreate(**{'id': 3, 'name': 'NevCFqq'})
    categories = crud.categories.create(db=db, obj_in=categories_data)
    assert categories.id is not None

    # Retrieve all records
    records = crud.categories.get_multi(db=db)
    assert len(records) > 0
    assert any(record.id == categories.id for record in records)


def test_get_by_id_categories(db):
    # Create a record first
    categories_data = schemas.CategoriesCreate(**{'id': 17, 'name': 'mIxm1YpSF'})
    categories = crud.categories.create(db=db, obj_in=categories_data)
    assert categories.id is not None

    # Retrieve the record by ID
    retrieved_categories = crud.categories.get(db=db, id=categories.id)
    assert retrieved_categories is not None
    assert retrieved_categories.id == categories.id
    assert retrieved_categories == categories


def test_delete_categories(db):
    # Create a record first
    categories_data = schemas.CategoriesCreate(**{'id': 17, 'name': ''})
    categories = crud.categories.create(db=db, obj_in=categories_data)
    assert categories.id is not None

    # Delete the record
    deleted_categories = crud.categories.remove(db=db, id=categories.id)
    assert deleted_categories is not None
    assert deleted_categories.id == categories.id

    # Ensure the record is no longer retrievable
    retrieved_categories = crud.categories.get(db=db, id=categories.id)
    assert retrieved_categories is None

# begin #
# ---write your code here--- #
# end #
