from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app import schemas
from app.services.deudas_service import DeudasService

from app.common.Utilidades.usuarios import get_current_user
from app.common.Utilidades.permisos import validar_rol, validar_pertenencia_ph


router = APIRouter(prefix="/{hp_id}/deudas", tags=["Deudas"])


@router.post("/", response_model=schemas.Deuda)
async def crear_deuda(
    hp_id: int,
    data: schemas.DeudaCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    usuario: dict = Depends(get_current_user)
):

    validar_pertenencia_ph(usuario, hp_id)
    validar_rol(usuario, ["ADMINISTRADOR", "ADMINISTRADOR INMOBILIARIO"])

    return await DeudasService.crear_deuda(db, data, background_tasks, hp_id)


@router.get("/", response_model=List[schemas.Deuda])
async def listar_deudas(
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

    return DeudasService.obtener_deudas(db, hp_id)


@router.get("/{deuda_id}", response_model=schemas.Deuda)
async def obtener_deuda(
    hp_id: int,
    deuda_id: int,
    db: Session = Depends(get_db),
    usuario: dict = Depends(get_current_user)
):
    validar_pertenencia_ph(usuario, hp_id)

    validar_rol(usuario, [
        "ADMINISTRADOR",
        "ADMINISTRADOR INMOBILIARIO",
        "PROPIETARIO TITULAR"
    ])

    return DeudasService.obtener_deuda(db, deuda_id, hp_id)


@router.delete("/{deuda_id}")
async def eliminar_deuda(
    hp_id: int,
    deuda_id: int,
    db: Session = Depends(get_db),
    usuario: dict = Depends(get_current_user)
):
    validar_pertenencia_ph(usuario, hp_id)
    validar_rol(usuario, ["ADMINISTRADOR"])

    return DeudasService.eliminar_deuda(db, deuda_id, hp_id)
