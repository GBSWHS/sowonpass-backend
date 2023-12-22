from typing import Any

from pydantic import BaseModel


class VerificationHistoryModelDTO(BaseModel):
    id: int
    user: Any
    assignee: Any
    process: Any
    process_group: Any
    status: int
    time_stamp: str


class VerificationHistoryInputDTO(BaseModel):
    user_id: int
    assignee_id: int
    process_id: int
    process_group_id: int
    status: int
    message: str
