from pydantic import BaseModel


class ProcessGroupModelDTO(BaseModel):
    id: int
    name: str
    description: str


class ProcessGroupModelInputDTO(BaseModel):
    name: str
    description: str
