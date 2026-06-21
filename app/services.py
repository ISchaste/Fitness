from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app import models

router = APIRouter(prefix="/api/additionalServices", tags=["Services"])


@router.get("")
def get_services(db: Session = Depends(get_db)):
    return db.query(models.Service).all()


@router.get("/{service_id}")
def get_service(service_id: str, db: Session = Depends(get_db)):
    s = db.query(models.Service).filter_by(id=service_id).first()

    return {
        "id": s.id,
        "name": s.name,
        "price": s.price,
        "clients": [c.id for c in db.query(models.Client).all() if s in c.services]
    }