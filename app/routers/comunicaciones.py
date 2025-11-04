from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app import schemas
from app.services.comunicacion_service import ComunicacionService

router = APIRouter(prefix="/comunicaciones", tags=["Comunicaciones"])


@router.post("/", response_model=schemas.ComunicacionCobro)
def crear_comunicacion(data: schemas.ComunicacionCobroCreate, db: Session = Depends(get_db)):
    return ComunicacionService.crear_comunicacion(db, data)


@router.get("/", response_model=list[schemas.ComunicacionCobro])
def obtener_comunicaciones(db: Session = Depends(get_db)):
    return ComunicacionService.obtener_comunicaciones(db)


@router.get("/propietario/{propietario_id}", response_model=list[schemas.ComunicacionCobro])
def historial_por_propietario(propietario_id: int, db: Session = Depends(get_db)):
    return ComunicacionService.obtener_historial_por_propietario(db, propietario_id)


@router.get("/deuda/{deuda_id}", response_model=list[schemas.ComunicacionCobro])
def historial_por_deuda(deuda_id: int, db: Session = Depends(get_db)):
    return ComunicacionService.obtener_historial_por_deuda(db, deuda_id)
