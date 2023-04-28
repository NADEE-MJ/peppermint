import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from src import crud
from src.core.config import settings
from src.models.user import User
from src.tests.utils.user import get_admin_auth_header
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

    user = await crud.user.get_by_email(db, email=email)

    await crud.user.remove(db, id=test_admin.id)
    await crud.user.remove(db, id=user.id)

    assert response.status_code == 200
    assert user
    assert user.email == email
    assert user.is_admin == is_admin


@pytest.mark.asyncio
async def test_remove_user(db: AsyncSession, client: TestClient, test_admin: User, test_user: User) -> None:
    headers = get_admin_auth_header(client)

    response = client.delete(
        f"{settings.API_VERSION_STR}/admin/user/{test_user.id}",
        headers=headers,
    )

    print(response.json())

    await crud.user.remove(db, id=test_admin.id)

    assert response.status_code == 200

    user = await crud.user.get_by_email(db, email=test_user.email)

    assert user is None


@pytest.mark.asyncio
async def test_admin_update_user_password(
    db: AsyncSession, client: TestClient, test_admin: User, test_user: User
) -> None:
    headers = get_admin_auth_header(client)

    new_name = "Test New Full Name"
    user_update = {"full_name": new_name}
    response = client.put(
        f"{settings.API_VERSION_STR}/admin/user/{test_user.id}",
        json=user_update,
        headers=headers,
    )
    res = response.json()

    await crud.user.remove(db, id=test_user.id)
    await crud.user.remove(db, id=test_admin.id)

    assert res["id"] == test_user.id
    assert res["full_name"] == new_name


@pytest.mark.asyncio
async def test_get_users_me(db: AsyncSession, client: TestClient, test_admin: User) -> None:
    headers = get_admin_auth_header(client)

    response = client.get(f"{settings.API_VERSION_STR}/admin", headers=headers)
    retrieved_admin = response.json()

    await crud.user.remove(db, id=test_admin.id)

    assert retrieved_admin
    assert retrieved_admin["id"] == test_admin.id
