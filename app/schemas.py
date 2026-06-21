from pydantic import BaseModel
from datetime import date


class ClientCreate(BaseModel):
    surname: str
    name: str
    patronymic: str | None
    birthday: date
    phone: str
    email: str


class TrainerCreate(BaseModel):
    surname: str
    name: str
    patronymic: str | None
    phone: str