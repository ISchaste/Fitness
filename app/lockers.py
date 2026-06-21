from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app import models

router = APIRouter(prefix="/api/lockers", tags=["Lockers"])


@router.get("")
def get_lockers(db: Session = Depends(get_db)):
    return [
        {
            "id": l.id,
            "number": l.number,
            "client_id": l.client_id,
            "status": "FREE" if not l.client_id else "BUSY"
        }
        for l in db.query(models.Locker).all()
    ]