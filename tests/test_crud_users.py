# begin #
# ---write your code here--- #
# end #

import schemas
import crud
from utils import pick_random_key_value
from fastapi.encoders import jsonable_encoder


def test_create_users(db):
    users_data = schemas.UsersCreate(**{'id': 4, 'username': 'VjPJ5sd', 'password': 'VXODEtTfi', 'is_superuser': True, 'role': 'o1h0Ojf6A'})
    users = crud.users.create(db=db, obj_in=users_data)
    data_json = pick_random_key_value(jsonable_encoder(users_data))
    test_json = jsonable_encoder(users)
    assert users.id is not None
    assert test_json[data_json[0]] == data_json[1]


def test_update_users(db):
    # Create a record first
    users_data = schemas.UsersCreate(**{'id': 6, 'username': 'XwDv8tdI', 'password': 'Aw8ZWZ', 'is_superuser': True, 'role': '8fCF4H'})
    users = crud.users.create(db=db, obj_in=users_data)
    assert users.id is not None

    # Update the record
    update_data = schemas.UsersUpdate(**{'id': 2, 'username': 'qudkEq', 'password': 'za4pmIxK', 'is_superuser': False, 'role': 'FR'})
    updated_users = crud.users.update(db=db, db_obj=users, obj_in=update_data)
    assert updated_users.id == users.id
    assert updated_users != users  # Ensure the record was actually updated


def test_get_users(db):
    # Create a record first
    users_data = schemas.UsersCreate(**{'id': 19, 'username': 'IoTJaN', 'password': '3QsgPZ', 'is_superuser': False, 'role': 'TT'})
    users = crud.users.create(db=db, obj_in=users_data)
    assert users.id is not None

    # Retrieve all records
    records = crud.users.get_multi(db=db)
    assert len(records) > 0
    assert any(record.id == users.id for record in records)


def test_get_by_id_users(db):
    # Create a record first
    users_data = schemas.UsersCreate(**{'id': 11, 'username': 'CPU9U9jm', 'password': 'Gp', 'is_superuser': False, 'role': 'DmXdwyb60L'})
    users = crud.users.create(db=db, obj_in=users_data)
    assert users.id is not None

    # Retrieve the record by ID
    retrieved_users = crud.users.get(db=db, id=users.id)
    assert retrieved_users is not None
    assert retrieved_users.id == users.id
    assert retrieved_users == users


def test_delete_users(db):
    # Create a record first
    users_data = schemas.UsersCreate(**{'id': 11, 'username': '', 'password': 'R', 'is_superuser': True, 'role': 'm8QjAEvgk'})
    users = crud.users.create(db=db, obj_in=users_data)
    assert users.id is not None

    # Delete the record
    deleted_users = crud.users.remove(db=db, id=users.id)
    assert deleted_users is not None
    assert deleted_users.id == users.id

    # Ensure the record is no longer retrievable
    retrieved_users = crud.users.get(db=db, id=users.id)
    assert retrieved_users is None

# begin #
# ---write your code here--- #
# end #
