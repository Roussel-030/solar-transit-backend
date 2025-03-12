# begin #
# ---write your code here--- #
# end #

import schemas
from core import security


def test_create_users_api(client, db):
    # Prepare User for connection
    user_data = {'email': 'test@example.com', 'password': 'testpassword'}
    user = schemas.Users(**user_data)
    db.add(user)
    db.commit()

    token = security.create_access_token(data={'id': str(user.id), 'email': user.email})
    users_data = {'id': 13, 'username': 'yQNb4', 'password': '', 'is_superuser': False, 'role': 'UooDS7KOpm'}
    response = client.post(
        '/api/v1/users/',
        users_in=users_data,
        headers={"Authorization": f'Bearer {token}'}
    )
    assert response.status_code == 200, response.text
    created_users = response.json()
    assert created_users['id'] is not None
    assert created_users['id'] == users_data['id']


def test_update_users_api(client, db):
    # Prepare User for connection
    user_data = {'email': 'test@example.com', 'password': 'testpassword'}
    user = schemas.Users(**user_data)
    db.add(user)
    db.commit()

    token = security.create_access_token(data={'id': str(user.id), 'email': user.email})
    # Create a record first
    users_data = {'id': 6, 'username': 'pOenDSO', 'password': '6DwYYLNC15', 'is_superuser': False, 'role': ''}
    create_response = client.post(
        '/api/v1/users/',
        users_in=users_data
    )
    assert create_response.status_code == 200, create_response.text
    created_users = create_response

    # Update the record
    update_data = {'id': 13, 'username': 'S4Jluwp', 'password': 'rdfV2n', 'is_superuser': True, 'role': ''}
    update_response = client.put(
        '/api/v1/users/',
        users_in=update_data,
        users_id=created_users.id,
        headers={"Authorization": f'Bearer {token}'}
    )
    assert update_response.status_code == 200, update_response.text
    updated_users = update_response
    assert updated_users.id == created_users.id
    assert updated_users != created_users  # Ensure the record was updated


def test_get_users_api(client, db):
    # Prepare User for connection
    user_data = {'email': 'test@example.com', 'password': 'testpassword'}
    user = schemas.Users(**user_data)
    db.add(user)
    db.commit()

    token = security.create_access_token(data={'id': str(user.id), 'email': user.email})
    # Create a record first
    users_data = {'id': 0, 'username': '72BrkbTo', 'password': 'Ws3', 'is_superuser': True, 'role': 'CWTaWfKv0p'}
    create_response = client.post(
        '/api/v1/users/',
        users_in=users_data,
        headers={"Authorization": f'Bearer {token}'}
    )
    assert create_response.status_code == 200, create_response.text
    created_users = create_response.json()

    # Retrieve all records
    get_response = client.get(
        '/api/v1/users/',
        headers={"Authorization": f'Bearer {token}'}
    )
    assert get_response.status_code == 200, get_response.text
    records = get_response.json()
    assert len(records) > 0
    assert any(record['id'] == created_users['id'] for record in records)


def test_get_by_id_users_api(client, db):
    # Prepare User for connection
    user_data = {'email': 'test@example.com', 'password': 'testpassword'}
    user = schemas.Users(**user_data)
    db.add(user)
    db.commit()

    token = security.create_access_token(data={'id': str(user.id), 'email': user.email})
    # Create a record first
    users_data = {'id': 16, 'username': '', 'password': '01h0t', 'is_superuser': False, 'role': 'Zkimpr3'}
    create_response = client.post(
        '/api/v1/users/',
        users_in=users_data,
        headers={"Authorization": f'Bearer {token}'}
    )
    assert create_response.status_code == 200, create_response.text
    created_users = create_response

    # Retrieve the record by ID
    get_response = client.get(
         '/api/v1/users/by_id/',
          users_id=created_users.id,
        headers={"Authorization": f'Bearer {token}'}
    )
    assert get_response.status_code == 200, get_response.text
    retrieved_users = get_response
    assert retrieved_users.id == created_users.id
    assert retrieved_users == created_users


def test_delete_users_api(client, db):
    # Prepare User for connection
    user_data = {'email': 'test@example.com', 'password': 'testpassword'}
    user = schemas.Users(**user_data)
    db.add(user)
    db.commit()

    token = security.create_access_token(data={'id': str(user.id), 'email': user.email})
    # Create a record first
    users_data = {'id': 19, 'username': 'f1BV2', 'password': 'OaMDph', 'is_superuser': False, 'role': 'MQh5zzr1'}
    create_response = client.post(
        '/api/v1/users/',
        users_in=users_data,
        headers={"Authorization": f'Bearer {token}'}
    )
    assert create_response.status_code == 200, create_response.text
    created_users = create_response

    # Delete the record
    delete_response = client.delete(
        '/api/v1/users/',
        users_id=created_users.id,
        headers={"Authorization": f'Bearer {token}'}
    )
    assert delete_response.status_code == 200, delete_response.text
    deleted_users = delete_response.json()
    assert deleted_users.id == created_users.id

    # Ensure the record is no longer retrievable
    get_response = client.get(
        '/api/v1/users/by_id/',
        users_id=created_users.id,
        headers={"Authorization": f'Bearer {token}'}
    )
    assert get_response.status_code == 404, get_response.text

# begin #
# ---write your code here--- #
# end #
