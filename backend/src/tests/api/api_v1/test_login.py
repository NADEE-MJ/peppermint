import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from src import crud
from src.core.config import settings
from src.models.user import User
from src.tests.utils.user import TEST_USER_EMAIL, TEST_USER_PASSWORD, get_auth_header
from src.utils import generate_password_reset_token


@pytest.mark.asyncio
async def test_get_access_token(db: AsyncSession, client: TestClient, test_user: User) -> None:
    login_data = {
        "username": TEST_USER_EMAIL,
        "password": TEST_USER_PASSWORD,
    }
    response = client.post(
        f"{settings.API_VERSION_STR}/login/access-token",
        data=login_data,
    )

    token = response.json()
    await crud.user.remove(db, id=test_user.id)
    assert response.status_code == 200
    assert "access_token" in token
    assert token["access_token"]


@pytest.mark.asyncio
async def test_use_access_token(db: AsyncSession, client: TestClient, test_user: User) -> None:
    headers = get_auth_header(client)
    response = client.post(f"{settings.API_VERSION_STR}/login/test-token", headers=headers)
    result = response.json()
    await crud.user.remove(db, id=test_user.id)
    print(result)
    assert response.status_code == 200
    assert "email" in result


@pytest.mark.asyncio
async def test_password_recovery_email(db: AsyncSession, client: TestClient, test_user: User) -> None:
    response = client.post(f"{settings.API_VERSION_STR}/password-recovery/{TEST_USER_EMAIL}")
    await crud.user.remove(db, id=test_user.id)
    assert response.json() == {"message": "Password recovery email sent"}


@pytest.mark.asyncio
async def test_reset_password(db: AsyncSession, client: TestClient, test_user: User) -> None:
    get_auth_header(client)
    token = generate_password_reset_token(email=TEST_USER_EMAIL)
    payload = {"new_password": "testpass", "token": token}
    response = client.post(f"{settings.API_VERSION_STR}/reset-password/", json=payload)
    await crud.user.remove(db, id=test_user.id)
    assert response.json() == {"message": "Password updated successfully"}
