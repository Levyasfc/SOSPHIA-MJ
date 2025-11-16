from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app import schemas
from app.services.votacion_service import VotacionService

router = APIRouter(prefix="/{hp_id}/votaciones", tags=["Votaciones"])

@router.post("/", response_model=schemas.Votacion)
def crear_votacion(
    hp_id: int,
    data: schemas.VotacionCreate,
    db: Session = Depends(get_db)
):
    return VotacionService.crear_votacion(db, data, hp_id)

@router.post("/{votacion_id}/votar", response_model=schemas.Votacion)
async def votar(
    hp_id: int,
    votacion_id: int,
    usuario_id: int,
    favor: int = 0,
    contra: int = 0,
    abstencion: int = 0,
    db: Session = Depends(get_db),
    background_tasks: BackgroundTasks = None
):
    return await VotacionService.votar(
        db=db,
        votacion_id=votacion_id,
        hp_id=hp_id,
        usuario_id=usuario_id,
        favor=favor,
        contra=contra,
        abstencion=abstencion,
        background_tasks=background_tasks
    )

@router.get("/", response_model=List[schemas.Votacion])
def listar_votaciones(hp_id: int, db: Session = Depends(get_db)):
    return VotacionService.obtener_votaciones(db, hp_id)