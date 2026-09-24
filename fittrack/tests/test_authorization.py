"""Unit tests for the reusable role-based authorization dependencies."""

import pytest

from fastapi import HTTPException

from backend.models.enums import UserRole
from backend.models.user import User

from backend.security.dependencies import (
    require_admin,
    require_member,
    require_trainer_or_admin,
)


def _user(role: UserRole) -> User:

    return User(
        id=1,
        username="test-user",
        email="test@example.com",
        password_hash="unused",
        role=role,
        is_active=True,
    )


def test_admin_dependency_allows_admin():

    assert (
        require_admin(
            _user(UserRole.ADMIN)
        ).role
        == UserRole.ADMIN
    )


def test_admin_dependency_rejects_member():

    with pytest.raises(
        HTTPException
    ) as exc:

        require_admin(
            _user(UserRole.MEMBER)
        )

    assert exc.value.status_code == 403


def test_trainer_or_admin_allows_both_roles():

    assert (
        require_trainer_or_admin(
            _user(UserRole.TRAINER)
        ).role
        == UserRole.TRAINER
    )

    assert (
        require_trainer_or_admin(
            _user(UserRole.ADMIN)
        ).role
        == UserRole.ADMIN
    )


def test_trainer_or_admin_rejects_member():

    with pytest.raises(
        HTTPException
    ) as exc:

        require_trainer_or_admin(
            _user(UserRole.MEMBER)
        )

    assert exc.value.status_code == 403


def test_member_dependency_rejects_admin():

    with pytest.raises(
        HTTPException
    ) as exc:

        require_member(
            _user(UserRole.ADMIN)
        )

    assert exc.value.status_code == 403