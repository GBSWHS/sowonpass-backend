from fastapi import APIRouter, Depends, HTTPException, status

from sowonpass_backend.db.dao.user_dao import UserDAO
from sowonpass_backend.db.models.user import UserModel
from sowonpass_backend.web.api.user.schema import UserModelDTO, UserModelInputDTO

router = APIRouter()


@router.get("/{user_id}", response_model=UserModelDTO)
async def get_user(user_id: int, user_dao: UserDAO = Depends()) -> UserModel:
    user = await user_dao.read_user(user_id=user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return user


@router.put("")
async def add_user(new_user: UserModelInputDTO, user_dao: UserDAO = Depends()) -> None:
    await user_dao.create_user(
        role=new_user.role,
        name=new_user.name,
        phone_number=new_user.phone_number,
    )


@router.delete("/{user_id}")
async def delete_user(user_id: int, user_dao: UserDAO = Depends()) -> None:
    await user_dao.delete_user(user_id=user_id)
