from api.deps import get_current_user
from core import security
from models import Users


def test_get_current_user(db, client):
    # Create a test user
    user_data = {"email": "test@example.com", "password": "testpassword"}
    user = Users(**user_data)
    db.add(user)
    db.commit()

    # Generate a token for the user
    token = security.create_access_token(data={"id": str(user.id), "email": user.email})

    # Test get_current_user
    current_user = get_current_user(db=db, token=token)
    assert current_user.email == user.email


def test_get_current_user(db, client):
    # Create a test user
    user_data = {"email": "test@example.com", "password": "testpassword", "is_active": True}
    user = Users(**user_data)
    db.add(user)
    db.commit()

    # Generate a token for the user
    token = security.create_access_token(data={"id": str(user.id), "email": user.email})

    # Test get_current_user
    current_user = get_current_user(current_user=user)
    assert current_user.is_active



