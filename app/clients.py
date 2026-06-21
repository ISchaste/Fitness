from uuid import UUID, uuid4

from fastapi import APIRouter, HTTPException

from app.models import (
    ClientCreate,
    ClientUpdate,
    ClientStatusUpdate,
    ClientResponse
)
from app.storage import clients, trainers

router = APIRouter(
    prefix="/api/clients",
    tags=["Clients"]
)


@router.post("", response_model=ClientResponse, status_code=201)
def create_client(data: ClientCreate):
    client_id = uuid4()

    client = {
        "id": client_id,
        "surname": data.surname,
        "name": data.name,
        "patronymic": data.patronymic,
        "birthday": data.birthday,
        "phone": data.phone,
        "email": data.email,
        "is_active": True,
        "trainer_id": None
    }

    clients[client_id] = client

    return client


@router.put("/{client_id}", response_model=ClientResponse)
def update_client(client_id: UUID, data: ClientUpdate):
    client = clients.get(client_id)

    if client is None:
        raise HTTPException(
            status_code=404,
            detail="Client not found"
        )

    client["surname"] = data.surname
    client["name"] = data.name
    client["patronymic"] = data.patronymic
    client["birthday"] = data.birthday
    client["phone"] = data.phone
    client["email"] = data.email

    return client


@router.get("", response_model=list[ClientResponse])
def get_all_clients():
    return list(clients.values())


@router.get("/{client_id}", response_model=ClientResponse)
def get_client(client_id: UUID):
    client = clients.get(client_id)

    if client is None:
        raise HTTPException(
            status_code=404,
            detail="Client not found"
        )

    return client


@router.get("/{client_id}/detail")
def get_client_detail(client_id: UUID):
    client = clients.get(client_id)

    if client is None:
        raise HTTPException(
            status_code=404,
            detail="Client not found"
        )

    trainer = None

    if client["trainer_id"] is not None:
        trainer = trainers.get(client["trainer_id"])

    return {
        **client,
        "trainer": trainer
    }


@router.patch("/{client_id}/status", response_model=ClientResponse)
def change_client_status(
        client_id: UUID,
        data: ClientStatusUpdate
):
    client = clients.get(client_id)

    if client is None:
        raise HTTPException(
            status_code=404,
            detail="Client not found"
        )

    client["is_active"] = data.is_active

    return client


@router.post("/{client_id}/trainer/{trainer_id}")
def assign_trainer(
        client_id: UUID,
        trainer_id: UUID
):
    client = clients.get(client_id)

    if client is None:
        raise HTTPException(
            status_code=404,
            detail="Client not found"
        )

    trainer = trainers.get(trainer_id)

    if trainer is None:
        raise HTTPException(
            status_code=404,
            detail="Trainer not found"
        )

    client["trainer_id"] = trainer_id

    return {
        "message": "Trainer assigned successfully",
        "client_id": client_id,
        "trainer_id": trainer_id
    }