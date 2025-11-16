from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session

from app.database import get_db
from app import schemas
from app.services.deudas_service import DeudasService

router = APIRouter(prefix="/{hp_id}/deudas", tags=["Deudas"])

@router.post("/", response_model=schemas.Deuda)
async def crear_deuda(
    hp_id: int,
    data: schemas.DeudaCreateSinHP,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    return await DeudasService.crear_deuda(db, data, background_tasks, hp_id)


@router.get("/", response_model=list[schemas.Deuda])
def obtener_deudas(hp_id: int, db: Session = Depends(get_db)):
    return DeudasService.obtener_deudas(db, hp_id)


@router.get("/{deuda_id}", response_model=schemas.Deuda)
def obtener_deuda(hp_id: int, deuda_id: int, db: Session = Depends(get_db)):
    return DeudasService.obtener_deuda(db, deuda_id, hp_id)


@router.put("/{deuda_id}", response_model=schemas.Deuda)
def actualizar_deuda(hp_id: int, deuda_id: int, data: schemas.DeudaUpdate, db: Session = Depends(get_db)):
    return DeudasService.actualizar_deuda(db, deuda_id, data, hp_id)


@router.delete("/{deuda_id}")
def eliminar_deuda(hp_id: int, deuda_id: int, db: Session = Depends(get_db)):
    return DeudasService.eliminar_deuda(db, deuda_id, hp_id)
