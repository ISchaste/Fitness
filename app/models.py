from sqlalchemy import Column, String, Boolean, Date, ForeignKey, Integer, Table
from sqlalchemy.orm import relationship
from app.database import Base


client_service = Table(
    "client_services",
    Base.metadata,
    Column("client_id", String, ForeignKey("clients.id")),
    Column("service_id", String, ForeignKey("services.id"))
)


class Trainer(Base):
    __tablename__ = "trainers"

    id = Column(String, primary_key=True)
    surname = Column(String)
    name = Column(String)
    patronymic = Column(String)
    phone = Column(String)
    status = Column(String, default="WORKING")

    clients = relationship("Client", back_populates="trainer")


class Locker(Base):
    __tablename__ = "lockers"

    id = Column(String, primary_key=True)
    number = Column(Integer, unique=True)
    client_id = Column(String, ForeignKey("clients.id"), nullable=True)


class Service(Base):
    __tablename__ = "services"

    id = Column(String, primary_key=True)
    name = Column(String)
    price = Column(Integer)


class Client(Base):
    __tablename__ = "clients"

    id = Column(String, primary_key=True)
    surname = Column(String)
    name = Column(String)
    patronymic = Column(String)
    birthday = Column(Date)
    phone = Column(String)
    email = Column(String)
    is_active = Column(Boolean, default=True)

    trainer_id = Column(String, ForeignKey("trainers.id"))
    locker_id = Column(String, ForeignKey("lockers.id"))

    trainer = relationship("Trainer", back_populates="clients")
    services = relationship("Service", secondary=client_service)