"""
tests/test_auth.py

End-to-end auth tests against an in-memory SQLite database (no MySQL
needed). Run with: pytest tests/test_auth.py -v
"""

import pytest

from fastapi.testclient import TestClient

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.database.session import (
    Base,
    get_db,
)

import backend.models  # noqa: F401

from backend.main import app
from backend.models.user import User


test_engine = create_engine(
    "sqlite:///:memory:",
    connect_args={
        "check_same_thread": False
    },
    poolclass=StaticPool,
)

TestSessionLocal = sessionmaker(
    bind=test_engine,
    autocommit=False,
    autoflush=False,
)

Base.metadata.create_all(
    bind=test_engine
)


def _override_get_db():

    db = TestSessionLocal()

    try:
        yield db

    finally:
        db.close()


app.dependency_overrides[
    get_db
] = _override_get_db


client = TestClient(app)


@pytest.fixture(autouse=True)
def clean_database():

    with test_engine.begin() as connection:

        for table in reversed(
            Base.metadata.sorted_tables
        ):

            connection.execute(
                table.delete()
            )

    yield


def _register(
    username="alice",
    email="alice@example.com",
    password="password123",
):

    return client.post(
        "/api/auth/register",
        json={
            "username": username,
            "email": email,
            "password": password,
            "first_name": "Alice",
            "last_name": "Anderson",
        },
    )


def test_register_creates_member_account():

    response = _register()

    assert response.status_code == 201

    body = response.json()

    assert body["username"] == "alice"
    assert body["role"] == "MEMBER"

    assert (
        body["member_profile"]["first_name"]
        == "Alice"
    )

    assert "password" not in body
    assert "password_hash" not in body


def test_register_rejects_duplicate_username():

    _register()

    assert (
        _register(
            email="someone-else@example.com"
        ).status_code
        == 409
    )


def test_register_rejects_duplicate_email():

    _register()

    assert (
        _register(
            username="someone_else"
        ).status_code
        == 409
    )


def test_login_with_username_returns_token():

    _register()

    response = client.post(
        "/api/auth/login",
        json={
            "username_or_email": "alice",
            "password": "password123",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["token_type"] == "bearer"
    assert len(body["access_token"]) > 20


def test_login_with_email_also_works():

    _register()

    response = client.post(
        "/api/auth/login",
        json={
            "username_or_email": "alice@example.com",
            "password": "password123",
        },
    )

    assert response.status_code == 200


def test_login_with_wrong_password_is_rejected():

    _register()

    response = client.post(
        "/api/auth/login",
        json={
            "username_or_email": "alice",
            "password": "the-wrong-password",
        },
    )

    assert response.status_code == 401


def test_login_with_unknown_user_is_rejected():

    response = client.post(
        "/api/auth/login",
        json={
            "username_or_email": "nobody-registered",
            "password": "whatever123",
        },
    )

    assert response.status_code == 401


def test_me_requires_authentication():

    assert (
        client.get("/api/auth/me").status_code
        == 401
    )


def test_me_rejects_garbage_token():

    response = client.get(
        "/api/auth/me",
        headers={
            "Authorization": "Bearer not-a-real-token"
        },
    )

    assert response.status_code == 401


def test_me_returns_current_user_with_valid_token():

    _register()

    login_response = client.post(
        "/api/auth/login",
        json={
            "username_or_email": "alice",
            "password": "password123",
        },
    )

    token = login_response.json()[
        "access_token"
    ]

    response = client.get(
        "/api/auth/me",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["username"] == "alice"

    assert (
        body["member_profile"]["first_name"]
        == "Alice"
    )


def test_passwords_are_hashed_not_stored_plain():

    _register()

    db = TestSessionLocal()

    try:

        user = (
            db.query(User)
            .filter(
                User.username == "alice"
            )
            .first()
        )

        assert (
            user.password_hash
            != "password123"
        )

        assert user.password_hash.startswith(
            (
                "$2a$",
                "$2b$",
            )
        )

    finally:
        db.close()


def _login(
    username_or_email="alice",
    password="password123",
):

    return client.post(
        "/api/auth/login",
        json={
            "username_or_email": username_or_email,
            "password": password,
        },
    )


def test_change_password_requires_authentication():

    response = client.post(
        "/api/auth/change-password",
        json={
            "current_password": "password123",
            "new_password": "newpassword123",
        },
    )

    assert response.status_code == 401


def test_change_password_updates_hash_and_allows_new_login():

    _register()

    token = _login().json()[
        "access_token"
    ]

    response = client.post(
        "/api/auth/change-password",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "current_password": "password123",
            "new_password": "newpassword123",
        },
    )

    assert response.status_code == 204

    assert (
        _login(
            password="password123"
        ).status_code
        == 401
    )

    assert (
        _login(
            password="newpassword123"
        ).status_code
        == 200
    )


def test_change_password_rejects_wrong_current_password():

    _register()

    token = _login().json()[
        "access_token"
    ]

    response = client.post(
        "/api/auth/change-password",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "current_password": "wrongpassword",
            "new_password": "newpassword123",
        },
    )

    assert response.status_code == 400


def test_change_password_rejects_same_password():

    _register()

    token = _login().json()[
        "access_token"
    ]

    response = client.post(
        "/api/auth/change-password",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "current_password": "password123",
            "new_password": "password123",
        },
    )

    assert response.status_code == 400


def test_inactive_user_cannot_access_me():

    _register()

    token = _login().json()[
        "access_token"
    ]

    db = TestSessionLocal()

    try:

        user = (
            db.query(User)
            .filter(
                User.username == "alice"
            )
            .first()
        )

        user.is_active = False

        db.commit()

    finally:
        db.close()

    response = client.get(
        "/api/auth/me",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 401