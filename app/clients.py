import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import models
from app.schemas import ClientCreate

router = APIRouter(prefix="/api/clients", tags=["Clients"])


@router.get("")
def get_clients(db: Session = Depends(get_db)):
    return db.query(models.Client).all()


@router.post("")
def create_client(data: ClientCreate, db: Session = Depends(get_db)):
    client = models.Client(id=str(uuid.uuid4()), **data.dict())
    db.add(client)
    db.commit()
    return client


@router.get("/{client_id}")
def get_client(client_id: str, db: Session = Depends(get_db)):
    client = db.query(models.Client).filter_by(id=client_id).first()
    if not client:
        raise HTTPException(404, "Client not found")
    return client


@router.put("/{client_id}")
def update_client(client_id: str, data: ClientCreate, db: Session = Depends(get_db)):
    client = db.query(models.Client).filter_by(id=client_id).first()
    if not client:
        raise HTTPException(404, "Client not found")

    for k, v in data.dict().items():
        setattr(client, k, v)

    db.commit()
    return client


@router.patch("/{client_id}/status")
def change_status(client_id: str, db: Session = Depends(get_db)):
    client = db.query(models.Client).filter(models.Client.id == client_id).first()

    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    client.is_active = not client.is_active

    db.commit()
    db.refresh(client)

    return {
        "id": client.id,
        "is_active": client.is_active
    }


@router.post("/{client_id}/trainer/{trainer_id}")
def assign_trainer(client_id: str, trainer_id: str, db: Session = Depends(get_db)):
    client = db.query(models.Client).filter_by(id=client_id).first()
    trainer = db.query(models.Trainer).filter_by(id=trainer_id).first()

    if not client:
        raise HTTPException(404, "Client not found")

    if not trainer:
        raise HTTPException(404, "Trainer not found")

    client.trainer_id = trainer_id
    db.commit()
    return {"status": "ok"}


@router.post("/{client_id}/locker/{locker_id}")
def assign_locker(client_id: str, locker_id: str, db: Session = Depends(get_db)):
    client = db.query(models.Client).filter_by(id=client_id).first()
    locker = db.query(models.Locker).filter_by(id=locker_id).first()

    if not client:
        raise HTTPException(404, "Client not found")

    if not locker:
        raise HTTPException(404, "Locker not found")

    if locker.client_id:
        raise HTTPException(409, "Locker already taken")

    if client.locker_id:
        old = db.query(models.Locker).filter_by(id=client.locker_id).first()
        if old:
            old.client_id = None

    locker.client_id = client.id
    client.locker_id = locker.id

    db.commit()
    return {"status": "locker assigned"}


@router.post("/{client_id}/additionalServices/{service_id}")
def add_service(client_id: str, service_id: str, db: Session = Depends(get_db)):
    client = db.query(models.Client).filter_by(id=client_id).first()
    service = db.query(models.Service).filter_by(id=service_id).first()

    if not client:
        raise HTTPException(404, "Client not found")

    if not service:
        raise HTTPException(404, "Service not found")

    if service in client.services:
        raise HTTPException(409, "Service already added")

    client.services.append(service)
    db.commit()

    return {"status": "service added"}


@router.get("/{client_id}/detail")
def detail(client_id: str, db: Session = Depends(get_db)):
    client = db.query(models.Client).filter_by(id=client_id).first()
    if not client:
        raise HTTPException(404, "Client not found")

    locker = db.query(models.Locker).filter_by(id=client.locker_id).first()

    return {
        "id": client.id,
        "surname": client.surname,
        "name": client.name,
        "patronymic": client.patronymic,
        "birthday": client.birthday,
        "phone": client.phone,
        "email": client.email,
        "is_active": client.is_active,
        "trainer": client.trainer,
        "locker": locker,
        "services": client.services
    }