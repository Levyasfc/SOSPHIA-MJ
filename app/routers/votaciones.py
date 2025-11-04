from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app import schemas
from app.services.votacion_service import VotacionService

router = APIRouter(prefix="/votaciones", tags=["Votaciones"])

@router.post("/", response_model=schemas.Votacion)
def crear_votacion(data: schemas.VotacionCreate, db: Session = Depends(get_db)):
    return VotacionService.crear_votacion(db, data)

@router.post("/{votacion_id}/votar", response_model=schemas.Votacion)
def votar(votacion_id: int, favor: int = 0, contra: int = 0, abstencion: int = 0, db: Session = Depends(get_db)):
    if (favor + contra + abstencion) == 0:
        raise HTTPException(status_code=400, detail="Se debe enviar al menos un voto")
    return VotacionService.votar(db, votacion_id, favor=favor, contra=contra, abstencion=abstencion)

@router.get("/", response_model=List[schemas.Votacion])
def listar_votaciones(db: Session = Depends(get_db)):
    return VotacionService.obtener_votaciones(db)
