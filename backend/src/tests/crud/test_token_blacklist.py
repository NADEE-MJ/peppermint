import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from src import crud
from src.models.token_blacklist import TokenBlacklistCreate
from src.tests.utils.token_blacklist import create_test_token_blacklist
from src.tests.utils.user import create_random_user
from src.tests.utils.utils import random_token


@pytest.mark.asyncio
async def test_create_token_blacklist(db: AsyncSession) -> None:
    user = await create_random_user(db)
    # code from create_test_token_blacklist copied for clarity
    token_blacklist = TokenBlacklistCreate(token=random_token())
    token_blacklist_from_db = await crud.token_blacklist.create(db, obj_in=token_blacklist, user_id=user.id)

    # ? deletes user and associated token_blacklists
    await crud.user.remove(db, id=user.id)
    assert token_blacklist_from_db
    assert token_blacklist_from_db.user_id == user.id


@pytest.mark.asyncio
async def test_get_all_token_blacklists_for_user(db: AsyncSession) -> None:
    user = await create_random_user(db)
    await create_test_token_blacklist(db, user_id=user.id)
    token_blacklists = await crud.token_blacklist.get_all_tokens_for_user(db, user_id=user.id)

    await crud.user.remove(db, id=user.id)
    assert len(token_blacklists) == 1
    assert token_blacklists[0].user_id == user.id


@pytest.mark.asyncio
async def test_get_token_blacklists_by_token(db: AsyncSession) -> None:
    user = await create_random_user(db)
    token = random_token()
    await create_test_token_blacklist(db, user_id=user.id, token=token)
    token_blacklist = await crud.token_blacklist.get_by_token(db, token=token)

    await crud.user.remove(db, id=user.id)
    assert token_blacklist.user_id == user.id
