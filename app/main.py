from fastapi import FastAPI

from app.database import engine, Base
from app import models
from app.utilidades.recordatoriosAuto import iniciar_scheduler

from app.routers import propietarios, deudas, comunicaciones, poderes, asambleas, votaciones

app = FastAPI(title="Microservicio Jurídico SOSPHIA", version="1.0")

Base.metadata.create_all(bind=engine)

iniciar_scheduler()

#IMPLEMENTACION DE LOS ROUTERS
app.include_router(propietarios.router)
app.include_router(deudas.router)
app.include_router(comunicaciones.router)
app.include_router(poderes.router)
app.include_router(asambleas.router)
app.include_router(votaciones.router)