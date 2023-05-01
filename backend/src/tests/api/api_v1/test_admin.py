import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from src import crud
from src.core.config import settings
from src.models.user import User
from src.tests.utils.user import get_admin_auth_header, create_random_user
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

    await crud.user.remove(db, id=user.id)

    assert response.status_code == 200
    assert user
    assert user.email == email
    assert user.is_admin == is_admin

@pytest.mark.asyncio
async def test_get_all_users(db: AsyncSession, client: TestClient, test_admin: User) -> None:
    headers = get_admin_auth_header(client)
    data = await crud.user.get_all(db)
    users = data["paginated_results"]

    for user in users:
        await crud.user.remove(db, id=user.id)

    user = await create_random_user(db)

    response = client.get(f"{settings.API_VERSION_STR}/admin/users", headers=headers)
    data = response.json()
    users = data["paginated_results"]
    total_pages = data["total_pages"]

    await crud.user.remove(db, id=user.id)

    assert len(users) == 1
    assert total_pages == 1


@pytest.mark.asyncio
async def test_remove_user(db: AsyncSession, client: TestClient, test_admin: User, test_user: User) -> None:
    headers = get_admin_auth_header(client)

    response = client.delete(
        f"{settings.API_VERSION_STR}/admin/user/{test_user.id}",
        headers=headers,
    )

    assert response.status_code == 200

    user = await crud.user.get_by_email(db, email=test_user.email)

    assert user is None


@pytest.mark.asyncio
async def test_admin_update_user(db: AsyncSession, client: TestClient, test_admin: User, test_user: User) -> None:
    headers = get_admin_auth_header(client)

    new_name = "Test New Full Name"
    user_update = {"full_name": new_name}
    response = client.put(
        f"{settings.API_VERSION_STR}/admin/user/{test_user.id}",
        json=user_update,
        headers=headers,
    )
    res = response.json()

    assert res["id"] == test_user.id
    assert res["full_name"] == new_name


@pytest.mark.asyncio
async def test_get_users_me(db: AsyncSession, client: TestClient, test_admin: User) -> None:
    headers = get_admin_auth_header(client)

    response = client.get(f"{settings.API_VERSION_STR}/admin", headers=headers)
    retrieved_admin = response.json()

    assert retrieved_admin
    assert retrieved_admin["id"] == test_admin.id


@pytest.mark.asyncio
async def test_get_user_by_email(db: AsyncSession, client: TestClient, test_admin: User, test_user: User) -> None:
    headers = get_admin_auth_header(client)

    response = client.get(f"{settings.API_VERSION_STR}/admin/user/{test_user.email}", headers=headers)
    user = response.json()

    assert user
    assert user["id"] == test_user.id


@pytest.mark.asyncio
async def test_update_admin_me(db: AsyncSession, client: TestClient, test_admin: User) -> None:
    headers = get_admin_auth_header(client)

    new_name = "Test New Full Name"
    data = {"full_name": new_name}
    response = client.put(f"{settings.API_VERSION_STR}/admin", headers=headers, json=data)
    admin = response.json()

    assert admin
    assert admin["id"] == test_admin.id
    assert admin["full_name"] == new_name
