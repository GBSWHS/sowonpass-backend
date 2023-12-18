import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from sowonpass_backend.db.dao.process_user_dao import ProcessUserDAO


@pytest.mark.anyio
async def test_create_process_user(
    dbsession: AsyncSession,
    test_user: int,
    test_process: int,
) -> None:
    process_user_dao = ProcessUserDAO(dbsession)

    await process_user_dao.create_process_user(
        user_id=test_user,
        process_id=test_process,
    )

    process_users = await process_user_dao.read_process_users(
        process_id=test_process,
    )
    assert len(process_users) == 1
    assert process_users[0].id == test_user


@pytest.mark.anyio
async def test_read_process_user(
    dbsession: AsyncSession,
    test_user: int,
    test_process: int,
) -> None:
    process_user_dao = ProcessUserDAO(dbsession)
    await process_user_dao.create_process_user(
        user_id=test_user,
        process_id=test_process,
    )

    process_users = await process_user_dao.read_process_users(
        process_id=test_process,
    )
    assert len(process_users) == 1
    assert process_users[0].id == test_user


@pytest.mark.anyio
async def test_delete_process_user(
    dbsession: AsyncSession,
    test_user: int,
    test_process: int,
) -> None:
    process_user_dao = ProcessUserDAO(dbsession)
    await process_user_dao.create_process_user(
        user_id=test_user,
        process_id=test_process,
    )

    await process_user_dao.delete_process_user(
        user_id=test_user,
        process_id=test_process,
    )

    process_users = await process_user_dao.read_process_users(
        process_id=test_process,
    )
    assert not process_users
