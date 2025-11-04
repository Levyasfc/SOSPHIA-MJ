from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app import schemas
from app.services.deudas_service import DeudasService

router = APIRouter(prefix="/deudas", tags=["Deudas"])


@router.post("/", response_model=schemas.Deuda)
def crear_deuda(data: schemas.DeudaCreate, db: Session = Depends(get_db)):
    return DeudasService.crear_deuda(db, data)


@router.get("/", response_model=list[schemas.Deuda])
def obtener_deudas(db: Session = Depends(get_db)):
    return DeudasService.obtener_deudas(db)


@router.get("/{deuda_id}", response_model=schemas.Deuda)
def obtener_deuda(deuda_id: int, db: Session = Depends(get_db)):
    return DeudasService.obtener_deuda(db, deuda_id)


@router.put("/{deuda_id}", response_model=schemas.Deuda)
def actualizar_deuda(deuda_id: int, data: schemas.DeudaUpdate, db: Session = Depends(get_db)):
    return DeudasService.actualizar_deuda(db, deuda_id, data)


@router.delete("/{deuda_id}")
def eliminar_deuda(deuda_id: int, db: Session = Depends(get_db)):
    return DeudasService.eliminar_deuda(db, deuda_id)
