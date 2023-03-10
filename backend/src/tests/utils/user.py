from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from src import crud
from src.core.config import settings
from src.models.user import User, UserCreate
from src.tests.utils.utils import random_email, random_lower_string, random_name

TEST_USER_NAME = "test user"
TEST_USER_EMAIL = "test@test.com"
TEST_USER_PASSWORD = "test"


async def create_test_user(db: AsyncSession) -> User:
    user = await crud.user.get_by_email(db, email=TEST_USER_EMAIL)
    if not user:
        user_create = UserCreate(
            full_name=TEST_USER_NAME,
            email=TEST_USER_EMAIL,
            password=TEST_USER_PASSWORD,
        )
        user = await crud.user.user_create(db, obj_in=user_create)

    return user


async def create_random_user(db: AsyncSession, password: str | None = None, is_active: bool = True) -> User:
    full_name = random_name()
    email = random_email()
    if password is None:
        password = random_lower_string()
    user_create = UserCreate(full_name=full_name, email=email, password=password)
    user = await crud.user.user_create(db=db, obj_in=user_create)
    if not is_active:
        user = await crud.user.user_update(db=db, db_obj=user, obj_in={"is_active": False})
    return user


def set_test_user_cookies(client: TestClient) -> None:
    login_data = {
        "email": TEST_USER_EMAIL,
        "password": TEST_USER_PASSWORD,
    }

    response = client.post(f"{settings.API_VERSION_STR}/login/access-token", json=login_data)
    client.cookies.set("fast_access_token", response.json()['access_token'])
