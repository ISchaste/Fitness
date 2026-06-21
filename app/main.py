from fastapi import FastAPI
from app.database import Base, engine, get_db
from app import clients, trainers, lockers, services, seed

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(clients.router)
app.include_router(trainers.router)
app.include_router(lockers.router)
app.include_router(services.router)


@app.on_event("startup")
def startup():
    db = next(get_db())
    seed.seed(db)