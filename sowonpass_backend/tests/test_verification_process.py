import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from sowonpass_backend.db.dao.verification_process_dao import VerificationProcessDAO
from sowonpass_backend.db.models.verification_process import VerificationProcessModel


@pytest.mark.anyio
async def test_create_read_delete_process(dbsession: AsyncSession) -> None:
    verification_process_dao = VerificationProcessDAO(dbsession)

    new_process = VerificationProcessModel(
        name="test_name",
        description="test_description",
    )

    await verification_process_dao.create_process(
        name=new_process.name,
        description=new_process.description,
    )
    process = await verification_process_dao.read_process(process_id=1)
    assert process is not None
    assert process.name == new_process.name
    assert process.description == new_process.description

    await verification_process_dao.delete_process(process_id=1)
    process = await verification_process_dao.read_process(process_id=1)
    assert process is None
