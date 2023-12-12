from pydantic import BaseModel


class UserModelDTO(BaseModel):
    id: int
    role: int
    name: str
    phone_number: str


class UserModelInputDTO(BaseModel):
    role: int
    name: str
    phone_number: str
