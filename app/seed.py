import uuid
from app.models import Locker, Service


def seed(db):
    if db.query(Locker).count() == 0:
        for i in range(1, 21):
            db.add(Locker(id=str(uuid.uuid4()), number=i))

    if db.query(Service).count() == 0:
        db.add_all([
            Service(id="SOLARIUM", name="Солярий", price=400),
            Service(id="POOL", name="Бассейн", price=200),
            Service(id="SAUNA", name="Сауна", price=0),
            Service(id="CRYOSAUNA", name="Криосауна", price=1000),
            Service(id="CROSSFIT", name="Кроссфит", price=500),
        ])

    db.commit()