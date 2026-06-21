from datetime import date
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class TrainerStatus(str, Enum):
    WORKING = "WORKING"
    ON_LEAVE = "ON_LEAVE"
    NOT_WORKING = "NOT_WORKING"


# =====================
# CLIENT
# =====================

class ClientCreate(BaseModel):
    surname: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1)
    patronymic: str | None = None
    birthday: date
    phone: str = Field(..., min_length=1)
    email: EmailStr


class ClientUpdate(BaseModel):
    surname: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1)
    patronymic: str | None = None
    birthday: date
    phone: str = Field(..., min_length=1)
    email: EmailStr


class ClientStatusUpdate(BaseModel):
    is_active: bool


class ClientResponse(BaseModel):
    id: UUID
    surname: str
    name: str
    patronymic: str | None
    birthday: date
    phone: str
    email: EmailStr
    is_active: bool
    trainer_id: UUID | None


# =====================
# TRAINER
# =====================

class TrainerCreate(BaseModel):
    surname: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1)
    patronymic: str | None = None
    phone: str = Field(..., min_length=1)


class TrainerUpdate(BaseModel):
    surname: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1)
    patronymic: str | None = None
    phone: str = Field(..., min_length=1)


class TrainerStatusUpdate(BaseModel):
    status: TrainerStatus


class TrainerResponse(BaseModel):
    id: UUID
    surname: str
    name: str
    patronymic: str | None
    phone: str
    status: TrainerStatus