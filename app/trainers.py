from uuid import UUID, uuid4

from fastapi import APIRouter, HTTPException

from app.models import (
    TrainerCreate,
    TrainerUpdate,
    TrainerStatusUpdate,
    TrainerResponse,
)
from app.storage import trainers, clients

router = APIRouter(
    prefix="/api/trainers",
    tags=["Trainers"]
)


@router.post("", response_model=TrainerResponse, status_code=201)
def create_trainer(data: TrainerCreate):
    trainer_id = uuid4()

    trainer = {
        "id": trainer_id,
        "surname": data.surname,
        "name": data.name,
        "patronymic": data.patronymic,
        "phone": data.phone,
        "status": "WORKING"
    }

    trainers[trainer_id] = trainer

    return trainer


@router.put("/{trainer_id}", response_model=TrainerResponse)
def update_trainer(trainer_id: UUID, data: TrainerUpdate):
    trainer = trainers.get(trainer_id)

    if trainer is None:
        raise HTTPException(
            status_code=404,
            detail="Trainer not found"
        )

    trainer["surname"] = data.surname
    trainer["name"] = data.name
    trainer["patronymic"] = data.patronymic
    trainer["phone"] = data.phone

    return trainer


@router.patch("/{trainer_id}/status", response_model=TrainerResponse)
def change_trainer_status(
        trainer_id: UUID,
        data: TrainerStatusUpdate
):
    trainer = trainers.get(trainer_id)

    if trainer is None:
        raise HTTPException(
            status_code=404,
            detail="Trainer not found"
        )

    trainer["status"] = data.status

    return trainer


@router.get("", response_model=list[TrainerResponse])
def get_all_trainers():
    return list(trainers.values())


@router.get("/{trainer_id}/detail")
def get_trainer_detail(trainer_id: UUID):
    trainer = trainers.get(trainer_id)

    if trainer is None:
        raise HTTPException(
            status_code=404,
            detail="Trainer not found"
        )

    trainer_clients = []

    for client in clients.values():
        if client.get("trainer_id") == trainer_id:
            trainer_clients.append(client)

    return {
        **trainer,
        "clients": trainer_clients
    }