import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app import models
from app.schemas import TrainerCreate

router = APIRouter(prefix="/api/trainers", tags=["Trainers"])


@router.get("")
def get_trainers(db: Session = Depends(get_db)):
    return db.query(models.Trainer).all()


@router.post("")
def create_trainer(data: TrainerCreate, db: Session = Depends(get_db)):
    trainer = models.Trainer(id=str(uuid.uuid4()), **data.dict())
    db.add(trainer)
    db.commit()
    return trainer


@router.get("/{trainer_id}")
def get_trainer(trainer_id: str, db: Session = Depends(get_db)):
    return db.query(models.Trainer).filter_by(id=trainer_id).first()


@router.put("/{trainer_id}")
def update_trainer(trainer_id: str, data: TrainerCreate, db: Session = Depends(get_db)):
    t = db.query(models.Trainer).filter_by(id=trainer_id).first()
    for k, v in data.dict().items():
        setattr(t, k, v)
    db.commit()
    return t


@router.patch("/{trainer_id}/status")
def status(trainer_id: str, db: Session = Depends(get_db)):
    t = db.query(models.Trainer).filter_by(id=trainer_id).first()
    t.status = "FIRED" if t.status == "WORKING" else "WORKING"
    db.commit()
    return t


@router.get("/{trainer_id}/detail")
def detail(trainer_id: str, db: Session = Depends(get_db)):
    t = db.query(models.Trainer).filter_by(id=trainer_id).first()
    return t