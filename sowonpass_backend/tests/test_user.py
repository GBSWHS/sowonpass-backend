import uuid

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from sowonpass_backend.db.dao.user_dao import UserDAO
from sowonpass_backend.web.api.user.schema import UserModelInputDTO


@pytest.mark.anyio
async def test_create_read_delete_user(dbsession: AsyncSession) -> None:
    user_dao = UserDAO(dbsession)

    test_uuid = uuid.uuid4().hex
    test_name = f"test_name-{test_uuid}"

    new_user = UserModelInputDTO(
        role=1,
        name=test_name,
        phone_number=test_uuid,
    )

    new_user_id = await user_dao.create_user(
        role=new_user.role,
        name=new_user.name,
        phone_number=new_user.phone_number,
    )

    user = await user_dao.read_user(user_id=new_user_id)
    assert user is not None
    assert user.role == new_user.role
    assert user.name == new_user.name
    assert user.phone_number == new_user.phone_number

    await user_dao.delete_user(user_id=new_user_id)
    user = await user_dao.read_user(user_id=new_user_id)
    assert user is None
