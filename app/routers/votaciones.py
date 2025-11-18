from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app import schemas
from app.services.votacion_service import VotacionService
from app.common.Utilidades.usuarios import get_current_user
from app.common.Utilidades.permisos import validar_rol, validar_pertenencia_ph

router = APIRouter(prefix="/{hp_id}/votaciones", tags=["Votaciones"])

@router.post("/", response_model=schemas.Votacion)
def crear_votacion(
    hp_id: int,
    data: schemas.VotacionCreate,
    db: Session = Depends(get_db)
):
    return VotacionService.crear_votacion(db, data, hp_id)

@router.post("/{votacion_id}/votar")
async def votar(
    hp_id: int,
    votacion_id: int,
    voto: str,
    db: Session = Depends(get_db),
    usuario: dict = Depends(get_current_user)
):
    validar_pertenencia_ph(usuario, hp_id)

    voto = voto.upper()
    if voto not in ["FAVOR", "CONTRA", "ABSTENCION"]:
        raise HTTPException(400, "El voto debe ser FAVOR / CONTRA / ABSTENCION")

    return VotacionService.votar(
        db=db,
        votacion_id=votacion_id,
        hp_id=hp_id,
        usuario_id=usuario["user_id"],
        voto=voto
    )

@router.get("/", response_model=List[schemas.Votacion])
def listar_votaciones(hp_id: int, db: Session = Depends(get_db)):
    return VotacionService.obtener_votaciones(db, hp_id)