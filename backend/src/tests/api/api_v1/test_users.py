import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from src import crud
from src.core.config import settings
from src.models.user import User
from src.tests.utils.user import TEST_USER_EMAIL, get_auth_header
from src.tests.utils.utils import random_email, random_lower_string, random_name


@pytest.mark.asyncio
async def test_get_users_me(db: AsyncSession, client: TestClient, test_user: User) -> None:
    headers = get_auth_header(client)
    response = client.get(f"{settings.API_VERSION_STR}/users/me", headers=headers)
    current_user = response.json()
    await crud.user.remove(db, id=test_user.id)  # type: ignore
    assert current_user
    assert current_user["email"] == TEST_USER_EMAIL


@pytest.mark.asyncio
async def test_update_user_me(db: AsyncSession, client: TestClient, test_user: User) -> None:
    headers = get_auth_header(client)
    user_update = {"password": "testpass"}
    response = client.put(
        f"{settings.API_VERSION_STR}/users/me",
        json=user_update,
        headers=headers,
    )
    current_user = response.json()
    await crud.user.remove(db, id=test_user.id)  # type: ignore
    assert current_user
    assert current_user["id"] == test_user.id
    assert current_user["email"] == test_user.email


@pytest.mark.asyncio
async def test_create_user_new_email(db: AsyncSession, client: TestClient, test_user: User) -> None:
    headers = get_auth_header(client)
    full_name = random_name()
    email = random_email()
    password = random_lower_string()
    data = {"full_name": full_name, "email": email, "password": password}
    response = client.post(
        f"{settings.API_VERSION_STR}/users/",
        json=data,
        headers=headers,
    )
    assert 200 <= response.status_code < 300
    user = await crud.user.get_by_email(db, email=email)
    await crud.user.remove(db, id=test_user.id)  # type: ignore
    assert user
    assert user.email == email


@pytest.mark.asyncio
async def test_create_user_existing_email(db: AsyncSession, client: TestClient, test_user: User) -> None:
    headers = get_auth_header(client)
    full_name = random_name()
    email = TEST_USER_EMAIL
    password = random_lower_string()
    data = {"full_name": full_name, "email": email, "password": password}
    response = client.post(
        f"{settings.API_VERSION_STR}/users/",
        json=data,
        headers=headers,
    )
    created_user = response.json()
    await crud.user.remove(db, id=test_user.id)  # type: ignore
    assert response.status_code == 400
    assert "email" not in created_user


@pytest.mark.asyncio
async def test_create_user_open_registration(db: AsyncSession, client: TestClient, test_user: User) -> None:
    headers = get_auth_header(client)
    full_name = random_name()
    email = random_email()
    password = random_lower_string()
    data = {"full_name": full_name, "email": email, "password": password}
    response = client.post(
        f"{settings.API_VERSION_STR}/users/open",
        json=data,
        headers=headers,
    )
    await crud.user.remove(db, id=test_user.id)  # type: ignore
    assert response.status_code == 200
    assert "email" in response.json()
