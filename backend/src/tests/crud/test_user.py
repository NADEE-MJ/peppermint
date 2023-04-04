import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from src import crud
from src.core.security import verify_password
from src.models.user import UserCreate, UserUpdate
from src.tests.utils.user import create_random_user
from src.tests.utils.utils import random_email, random_lower_string, random_name


@pytest.mark.asyncio
async def test_create_user(db: AsyncSession) -> None:
    # code from create_random_user copied for clarity
    full_name = random_name()
    email = random_email()
    password = random_lower_string()
    user_create = UserCreate(full_name=full_name, email=email, password=password)
    user = await crud.user.create(db, obj_in=user_create)
    await crud.user.remove(db, id=user.id)  # type: ignore
    assert hasattr(user, "password")


@pytest.mark.asyncio
async def test_authenticate_user(db: AsyncSession) -> None:
    password = random_lower_string()
    user = await create_random_user(db, password)
    authenticated_user = await crud.user.authenticate(db, email=user.email, password=password)
    await crud.user.remove(db, id=user.id)  # type: ignore
    if authenticated_user is not None:
        assert user.email == authenticated_user.email
    else:
        assert False


@pytest.mark.asyncio
async def test_not_authenticate_user(db: AsyncSession) -> None:
    password = random_lower_string()
    user = await create_random_user(db, password)
    password = "wrong password"
    non_authenticated_user = await crud.user.authenticate(db, email=user.email, password=password)
    await crud.user.remove(db, id=user.id)  # type: ignore
    assert non_authenticated_user is None


@pytest.mark.asyncio
async def test_check_if_user_is_active(db: AsyncSession) -> None:
    user = await create_random_user(db)
    is_active = crud.user.is_active(user)
    await crud.user.remove(db, id=user.id)  # type: ignore
    assert is_active is True


@pytest.mark.asyncio
async def test_check_if_user_is_active_inactive(db: AsyncSession) -> None:
    user = await create_random_user(db, is_active=False)
    is_active = crud.user.is_active(user)
    await crud.user.remove(db, id=user.id)  # type: ignore
    assert is_active is False


@pytest.mark.asyncio
async def test_get_user(db: AsyncSession) -> None:
    user = await create_random_user(db)
    user_from_db = await crud.user.get(db, id=user.id)
    await crud.user.remove(db, id=user.id)  # type: ignore
    assert user_from_db
    assert user.email == user_from_db.email


@pytest.mark.asyncio
async def test_get_user_by_email(db: AsyncSession) -> None:
    user = await create_random_user(db)
    user_from_db = await crud.user.get_by_email(db, email=user.email)
    await crud.user.remove(db, id=user.id)  # type: ignore
    assert user_from_db
    assert user.email == user_from_db.email


@pytest.mark.asyncio
async def test_update_user(db: AsyncSession) -> None:
    user = await create_random_user(db)
    new_password = random_lower_string()
    user_create_update = UserUpdate(password=new_password)
    user_from_db = await crud.user.update(db, db_obj=user, obj_in=user_create_update)
    await crud.user.remove(db, id=user.id)  # type: ignore
    assert user_from_db
    assert user.email == user_from_db.email
    assert verify_password(new_password, user_from_db.password)
