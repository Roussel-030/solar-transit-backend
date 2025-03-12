# begin #
# ---write your code here--- #
# end #

import schemas
from core import security


def test_create_listings_api(client, db):
    # Prepare User for connection
    user_data = {'email': 'test@example.com', 'password': 'testpassword'}
    user = schemas.Users(**user_data)
    db.add(user)
    db.commit()

    token = security.create_access_token(data={'id': str(user.id), 'email': user.email})
    listings_data = {'id': 4, 'name': '7mUWSe', 'description': 'KracZCH3XOQ', 'address': 'gd7g2nz5', 'latitude': 3.5138504590132604, 'category_id': 6, 'created_by': 16}
    response = client.post(
        '/api/v1/listings/',
        listings_in=listings_data,
        headers={"Authorization": f'Bearer {token}'}
    )
    assert response.status_code == 200, response.text
    created_listings = response.json()
    assert created_listings['id'] is not None
    assert created_listings['id'] == listings_data['id']


def test_update_listings_api(client, db):
    # Prepare User for connection
    user_data = {'email': 'test@example.com', 'password': 'testpassword'}
    user = schemas.Users(**user_data)
    db.add(user)
    db.commit()

    token = security.create_access_token(data={'id': str(user.id), 'email': user.email})
    # Create a record first
    listings_data = {'id': 7, 'name': 'gb', 'description': 'DeZBWQI9O8ysMDQ', 'address': 'bzI2', 'latitude': 3.969799634389409, 'category_id': 15, 'created_by': 3}
    create_response = client.post(
        '/api/v1/listings/',
        listings_in=listings_data
    )
    assert create_response.status_code == 200, create_response.text
    created_listings = create_response

    # Update the record
    update_data = {'id': 14, 'name': '9FxvY', 'description': 'QVUC4VzLUz1cVfNNNuvnPyDm7lI7oAU', 'address': 'FUTI1d', 'latitude': 2.799521231102646, 'category_id': 10, 'created_by': 6}
    update_response = client.put(
        '/api/v1/listings/',
        listings_in=update_data,
        listings_id=created_listings.id,
        headers={"Authorization": f'Bearer {token}'}
    )
    assert update_response.status_code == 200, update_response.text
    updated_listings = update_response
    assert updated_listings.id == created_listings.id
    assert updated_listings != created_listings  # Ensure the record was updated


def test_get_listings_api(client, db):
    # Prepare User for connection
    user_data = {'email': 'test@example.com', 'password': 'testpassword'}
    user = schemas.Users(**user_data)
    db.add(user)
    db.commit()

    token = security.create_access_token(data={'id': str(user.id), 'email': user.email})
    # Create a record first
    listings_data = {'id': 13, 'name': 'QP', 'description': 'S', 'address': 'QiqKXYPeO', 'latitude': 5.2766228915858235, 'category_id': 9, 'created_by': 12}
    create_response = client.post(
        '/api/v1/listings/',
        listings_in=listings_data,
        headers={"Authorization": f'Bearer {token}'}
    )
    assert create_response.status_code == 200, create_response.text
    created_listings = create_response.json()

    # Retrieve all records
    get_response = client.get(
        '/api/v1/listings/',
        headers={"Authorization": f'Bearer {token}'}
    )
    assert get_response.status_code == 200, get_response.text
    records = get_response.json()
    assert len(records) > 0
    assert any(record['id'] == created_listings['id'] for record in records)


def test_get_by_id_listings_api(client, db):
    # Prepare User for connection
    user_data = {'email': 'test@example.com', 'password': 'testpassword'}
    user = schemas.Users(**user_data)
    db.add(user)
    db.commit()

    token = security.create_access_token(data={'id': str(user.id), 'email': user.email})
    # Create a record first
    listings_data = {'id': 9, 'name': 'fKjV', 'description': 'e8dkCTQzsH3chsqPA3UvHyXtSf8dFrnb91fejPZbZ', 'address': '6', 'latitude': 3.670960805431479, 'category_id': 4, 'created_by': 18}
    create_response = client.post(
        '/api/v1/listings/',
        listings_in=listings_data,
        headers={"Authorization": f'Bearer {token}'}
    )
    assert create_response.status_code == 200, create_response.text
    created_listings = create_response

    # Retrieve the record by ID
    get_response = client.get(
         '/api/v1/listings/by_id/',
          listings_id=created_listings.id,
        headers={"Authorization": f'Bearer {token}'}
    )
    assert get_response.status_code == 200, get_response.text
    retrieved_listings = get_response
    assert retrieved_listings.id == created_listings.id
    assert retrieved_listings == created_listings


def test_delete_listings_api(client, db):
    # Prepare User for connection
    user_data = {'email': 'test@example.com', 'password': 'testpassword'}
    user = schemas.Users(**user_data)
    db.add(user)
    db.commit()

    token = security.create_access_token(data={'id': str(user.id), 'email': user.email})
    # Create a record first
    listings_data = {'id': 10, 'name': 'mX6', 'description': 'OY', 'address': '', 'latitude': 4.413640809698741, 'category_id': 7, 'created_by': 15}
    create_response = client.post(
        '/api/v1/listings/',
        listings_in=listings_data,
        headers={"Authorization": f'Bearer {token}'}
    )
    assert create_response.status_code == 200, create_response.text
    created_listings = create_response

    # Delete the record
    delete_response = client.delete(
        '/api/v1/listings/',
        listings_id=created_listings.id,
        headers={"Authorization": f'Bearer {token}'}
    )
    assert delete_response.status_code == 200, delete_response.text
    deleted_listings = delete_response.json()
    assert deleted_listings.id == created_listings.id

    # Ensure the record is no longer retrievable
    get_response = client.get(
        '/api/v1/listings/by_id/',
        listings_id=created_listings.id,
        headers={"Authorization": f'Bearer {token}'}
    )
    assert get_response.status_code == 404, get_response.text

# begin #
# ---write your code here--- #
# end #
