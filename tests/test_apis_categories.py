# begin #
# ---write your code here--- #
# end #

import schemas
from core import security


def test_create_categories_api(client, db):
    # Prepare User for connection
    user_data = {'email': 'test@example.com', 'password': 'testpassword'}
    user = schemas.Users(**user_data)
    db.add(user)
    db.commit()

    token = security.create_access_token(data={'id': str(user.id), 'email': user.email})
    categories_data = {'id': 18, 'name': 'lP9tJgSFB'}
    response = client.post(
        '/api/v1/categories/',
        categories_in=categories_data,
        headers={"Authorization": f'Bearer {token}'}
    )
    assert response.status_code == 200, response.text
    created_categories = response.json()
    assert created_categories['id'] is not None
    assert created_categories['id'] == categories_data['id']


def test_update_categories_api(client, db):
    # Prepare User for connection
    user_data = {'email': 'test@example.com', 'password': 'testpassword'}
    user = schemas.Users(**user_data)
    db.add(user)
    db.commit()

    token = security.create_access_token(data={'id': str(user.id), 'email': user.email})
    # Create a record first
    categories_data = {'id': 1, 'name': 'CuV'}
    create_response = client.post(
        '/api/v1/categories/',
        categories_in=categories_data
    )
    assert create_response.status_code == 200, create_response.text
    created_categories = create_response

    # Update the record
    update_data = {'id': 2, 'name': 'qqx'}
    update_response = client.put(
        '/api/v1/categories/',
        categories_in=update_data,
        categories_id=created_categories.id,
        headers={"Authorization": f'Bearer {token}'}
    )
    assert update_response.status_code == 200, update_response.text
    updated_categories = update_response
    assert updated_categories.id == created_categories.id
    assert updated_categories != created_categories  # Ensure the record was updated


def test_get_categories_api(client, db):
    # Prepare User for connection
    user_data = {'email': 'test@example.com', 'password': 'testpassword'}
    user = schemas.Users(**user_data)
    db.add(user)
    db.commit()

    token = security.create_access_token(data={'id': str(user.id), 'email': user.email})
    # Create a record first
    categories_data = {'id': 19, 'name': 'qDoMh22SqG'}
    create_response = client.post(
        '/api/v1/categories/',
        categories_in=categories_data,
        headers={"Authorization": f'Bearer {token}'}
    )
    assert create_response.status_code == 200, create_response.text
    created_categories = create_response.json()

    # Retrieve all records
    get_response = client.get(
        '/api/v1/categories/',
        headers={"Authorization": f'Bearer {token}'}
    )
    assert get_response.status_code == 200, get_response.text
    records = get_response.json()
    assert len(records) > 0
    assert any(record['id'] == created_categories['id'] for record in records)


def test_get_by_id_categories_api(client, db):
    # Prepare User for connection
    user_data = {'email': 'test@example.com', 'password': 'testpassword'}
    user = schemas.Users(**user_data)
    db.add(user)
    db.commit()

    token = security.create_access_token(data={'id': str(user.id), 'email': user.email})
    # Create a record first
    categories_data = {'id': 4, 'name': 'q5Xyhutr9P'}
    create_response = client.post(
        '/api/v1/categories/',
        categories_in=categories_data,
        headers={"Authorization": f'Bearer {token}'}
    )
    assert create_response.status_code == 200, create_response.text
    created_categories = create_response

    # Retrieve the record by ID
    get_response = client.get(
         '/api/v1/categories/by_id/',
          categories_id=created_categories.id,
        headers={"Authorization": f'Bearer {token}'}
    )
    assert get_response.status_code == 200, get_response.text
    retrieved_categories = get_response
    assert retrieved_categories.id == created_categories.id
    assert retrieved_categories == created_categories


def test_delete_categories_api(client, db):
    # Prepare User for connection
    user_data = {'email': 'test@example.com', 'password': 'testpassword'}
    user = schemas.Users(**user_data)
    db.add(user)
    db.commit()

    token = security.create_access_token(data={'id': str(user.id), 'email': user.email})
    # Create a record first
    categories_data = {'id': 9, 'name': 'cektf'}
    create_response = client.post(
        '/api/v1/categories/',
        categories_in=categories_data,
        headers={"Authorization": f'Bearer {token}'}
    )
    assert create_response.status_code == 200, create_response.text
    created_categories = create_response

    # Delete the record
    delete_response = client.delete(
        '/api/v1/categories/',
        categories_id=created_categories.id,
        headers={"Authorization": f'Bearer {token}'}
    )
    assert delete_response.status_code == 200, delete_response.text
    deleted_categories = delete_response.json()
    assert deleted_categories.id == created_categories.id

    # Ensure the record is no longer retrievable
    get_response = client.get(
        '/api/v1/categories/by_id/',
        categories_id=created_categories.id,
        headers={"Authorization": f'Bearer {token}'}
    )
    assert get_response.status_code == 404, get_response.text

# begin #
# ---write your code here--- #
# end #
