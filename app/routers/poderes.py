from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app import schemas
from app.services.poder_service import PoderService

from app.common.Utilidades.usuarios import get_current_user
from app.common.Utilidades.permisos import validar_rol, validar_pertenencia_ph

router = APIRouter(prefix="/{hp_id}/poderes", tags=["Poderes"])


@router.post("/", response_model=schemas.Poder)
async def crear_poder(
    hp_id: int,
    data: schemas.PoderCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    usuario: dict = Depends(get_current_user)
):
    validar_pertenencia_ph(usuario, hp_id)

    validar_rol(usuario, ["PROPIETARIO TITULAR"])

    return await PoderService.crear_poder(
        db, data, hp_id, usuario["email"], background_tasks
    )


@router.get("/", response_model=List[schemas.Poder])
async def listar_poderes(
    hp_id: int,
    db: Session = Depends(get_db),
    usuario: dict = Depends(get_current_user)
):
    validar_pertenencia_ph(usuario, hp_id)

    validar_rol(usuario, [
        "ADMINISTRADOR",
        "ADMINISTRADOR INMOBILIARIO",
        "PROPIETARIO TITULAR"
    ])

    return PoderService.obtener_poderes(db, hp_id)


@router.delete("/{poder_id}")
async def eliminar_poder(
    hp_id: int,
    poder_id: int,
    db: Session = Depends(get_current_user),
    usuario: dict = Depends(get_current_user)
):
    validar_pertenencia_ph(usuario, hp_id)

    validar_rol(usuario, [
        "ADMINISTRADOR",
        "ADMINISTRADOR INMOBILIARIO",
        "PROPIETARIO TITULAR"
    ])

    return PoderService.eliminar_poder(db, poder_id, hp_id)
