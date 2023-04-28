import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from src import crud
from src.core.config import settings
from src.models.user import User
from src.tests.utils.user import create_random_user, get_admin_auth_header
from src.tests.utils.utils import random_email, random_lower_string, random_name


@pytest.mark.asyncio
async def test_create_new_admin(db: AsyncSession, client: TestClient, test_admin: User) -> None:
    headers = get_admin_auth_header(client)
    full_name = random_name()
    email = random_email()
    password = random_lower_string()
    is_admin = True
    data = {"full_name": full_name, "email": email, "password": password}
    response = client.post(
        f"{settings.API_VERSION_STR}/admin?is_admin={is_admin}",
        json=data,
        headers=headers,
    )
    assert response.status_code == 200
    user = await crud.user.get_by_email(db, email=email)
    await crud.user.remove(db, id=test_admin.id)
    await crud.user.remove(db, id=user.id)
    assert user
    assert user.email == email
    assert user.is_admin == is_admin


@pytest.mark.asyncio
async def test_remove_user(db: AsyncSession, client: TestClient, test_admin: User) -> None:
    headers = get_admin_auth_header(client)
    full_name = random_name()
    email = random_email()
    password = random_lower_string()
    is_admin = False
    data = {"full_name": full_name, "email": email, "password": password}
    response = client.post(
        f"{settings.API_VERSION_STR}/admin?is_admin={is_admin}",
        json=data,
        headers=headers,
    )

    user = await crud.user.get_by_email(db, email=email)
    user_id = user.id

    response = client.delete(
        f"{settings.API_VERSION_STR}/admin?user_id={user_id}",
        json=data,
        headers=headers,
    )
    assert response.status_code == 200
    await crud.user.remove(db, id=test_admin.id)

    user = await crud.user.get_by_email(db, email=email)
    assert user == None


@pytest.mark.asyncio
async def test_admin_update_user(db: AsyncSession, client: TestClient, test_admin: User) -> None:
    headers = get_admin_auth_header(client)
    full_name = random_name()
    email = random_email()
    password = random_lower_string()
    is_admin = False

    #Creates the test user
    data = {"full_name": full_name, "email": email, "password": password}
    response = client.post(
        f"{settings.API_VERSION_STR}/admin?is_admin={is_admin}",
        json=data,
        headers=headers,
    )

    #Accesses new test user
    user_to_update = await crud.user.get_by_email(db, email=email)

    #Update the accessed user
    user_update = {"password": "testpass"}
    response = client.put(
        f"{settings.API_VERSION_STR}/admin/user/{user_to_update.id}",
        json=user_update,
        headers=headers,
    )

    test_user = response.json()
    await crud.user.remove(db, id=user_to_update.id)
    await crud.user.remove(db, id=test_admin.id) #Removes the test admin created
    assert user_to_update
    assert user_to_update.id == test_user["id"]
    assert user_to_update.email == test_user["email"]


@pytest.mark.asyncio
async def test_get_users_me(db: AsyncSession, client: TestClient, test_admin: User) -> None:
    headers = get_admin_auth_header(client)
    user = await create_random_user(db)
    response = client.get(f"{settings.API_VERSION_STR}/admin/{user.id}", headers=headers)
    retrieved_user = response.json()
    await crud.user.remove(db, id=test_admin.id)
    await crud.user.remove(db, id=user.id)
    assert retrieved_user
    assert retrieved_user["id"] == user.id