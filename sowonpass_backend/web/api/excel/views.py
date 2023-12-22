from datetime import datetime

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from fastapi.responses import Response

from sowonpass_backend.db.dao.process_assignee_dao import ProcessAssigneeDAO
from sowonpass_backend.db.dao.process_user_dao import ProcessUserDAO
from sowonpass_backend.db.dao.user_dao import UserDAO
from sowonpass_backend.db.dao.verification_process_dao import VerificationProcessDAO
from sowonpass_backend.db.enum.user_role import UserRole
from sowonpass_backend.web.api.excel.utils import (
    create_excel_file_from_user_data,
    parse_excel_file,
)

router = APIRouter()


@router.post("/users")
async def upload_users(
    file: UploadFile = File(...),
    user_dao: UserDAO = Depends(),
) -> None:
    datas = parse_excel_file(file, {"name", "phone_number"})

    for user_dict in datas["users"]:
        name = user_dict.get("name")
        phone_number = user_dict.get("phone_number").replace("-", "")

        user_exist = await user_dao.read_user_by_info(name, phone_number)
        if user_exist:
            continue
        await user_dao.create_user(name, phone_number, UserRole.USER.value)


@router.get("/users")
async def download_users(user_dao: UserDAO = Depends()) -> Response:
    users = await user_dao.read_all_users()

    excel_file = create_excel_file_from_user_data(
        users,
        required_fields={"name", "phone_number"},
        default_rows=[{"name": "홍길동", "phone_number": "010-1111-2222"}],
    )

    timestamp = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    filename = f"users-{timestamp}.xlsx"

    return Response(
        content=excel_file.read(),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )


@router.post("/group/{process_group_id}")
async def upload_processes(  # noqa: WPS210, WPS211
    process_group_id: int,
    file: UploadFile = File(...),
    user_dao: UserDAO = Depends(),
    process_dao: VerificationProcessDAO = Depends(),
    process_user_dao: ProcessUserDAO = Depends(),
    process_assignee_dao: ProcessAssigneeDAO = Depends(),
) -> None:
    all_sheets_data = parse_excel_file(file, {"이름", "전화번호"})

    await process_dao.delete_process_by_group_id(process_group_id)

    for sheet_name, data in all_sheets_data.items():
        process_id = await process_dao.create_process_with_group_id(
            sheet_name,
            "",
            process_group_id,
        )

        for row in data:
            name = str(row.get("이름"))
            phone_number = str(row.get("전화번호")).replace("-", "")
            is_assignee = row.get("colored")

            user = await user_dao.read_user_by_info(name, phone_number)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"User '{name}({phone_number})' not found.",
                )

            if is_assignee:
                await process_assignee_dao.create_process_assignee(
                    process_id=process_id,
                    user_id=user.id,
                )
                # TODO add additional user info
            else:
                await process_user_dao.create_process_user(
                    process_id=process_id,
                    user_id=user.id,
                )


# TODO add download processes endpoint
