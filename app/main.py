from fastapi import FastAPI
from app.database import engine, Base

from app.routers import propietarios, deudas

app = FastAPI(title="Microservicio Jurídico SOSPHIA", version="1.0")

Base.metadata.create_all(bind=engine)

app.include_router(propietarios.router)
app.include_router(deudas.router)