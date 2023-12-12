from pydantic import BaseModel


class VerificationProcessModelDTO(BaseModel):
    id: int
    name: str
    description: str
    process_group_id: int | None


class VerificationProcessModelInputDTO(BaseModel):
    name: str
    description: str
