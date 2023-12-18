import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from sowonpass_backend.db.dao.process_assignee_dao import ProcessAssigneeDAO


@pytest.mark.anyio
async def test_create_process_assignee(
    dbsession: AsyncSession,
    test_user: int,
    test_process: int,
) -> None:
    user_id = test_user
    process_id = test_process

    process_assignee_dao = ProcessAssigneeDAO(dbsession)

    await process_assignee_dao.create_process_assignee(
        user_id=user_id,
        process_id=process_id,
    )

    process_assignees = await process_assignee_dao.read_process_assignees(
        process_id=process_id,
    )
    assert len(process_assignees) == 1
    assert process_assignees[0].id == user_id


@pytest.mark.anyio
async def test_read_process_assignee(
    dbsession: AsyncSession,
    test_user: int,
    test_process: int,
) -> None:
    process_assignee_dao = ProcessAssigneeDAO(dbsession)
    await process_assignee_dao.create_process_assignee(
        user_id=test_user,
        process_id=test_process,
    )

    process_assignees = await process_assignee_dao.read_process_assignees(
        process_id=test_process,
    )
    assert len(process_assignees) == 1
    assert process_assignees[0].id == test_user


@pytest.mark.anyio
async def test_delete_process_assignee(
    dbsession: AsyncSession,
    test_user: int,
    test_process: int,
) -> None:
    process_assignee_dao = ProcessAssigneeDAO(dbsession)
    await process_assignee_dao.create_process_assignee(
        user_id=test_user,
        process_id=test_process,
    )

    await process_assignee_dao.delete_process_assignee(
        user_id=test_user,
        process_id=test_process,
    )

    process_assignees = await process_assignee_dao.read_process_assignees(
        process_id=test_process,
    )
    assert not process_assignees
