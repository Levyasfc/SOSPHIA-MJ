from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app import schemas
from app.services.propietario_service import PropietarioService

router = APIRouter(prefix="/propietarios", tags=["Propietarios"])

@router.post("/", response_model=schemas.Propietario)
def crear_propietario(data: schemas.PropietarioCreate, db: Session = Depends(get_db)):
    return PropietarioService.crear_propietario(db, data)

@router.get("/", response_model=List[schemas.Propietario])
def obtener_propietarios(db: Session = Depends(get_db)):
    return PropietarioService.obtener_propietarios(db)

@router.get("/{propietario_id}", response_model=schemas.Propietario)
def obtener_propietario(propietario_id: int, db: Session = Depends(get_db)):
    return PropietarioService.obtener_propietario(db, propietario_id)

@router.put("/{propietario_id}", response_model=schemas.Propietario)
def actualizar_propietario(propietario_id: int, data: schemas.PropietarioUpdate, db: Session = Depends(get_db)):
    return PropietarioService.actualizar_propietario(db, propietario_id, data)

@router.delete("/{propietario_id}")
def eliminar_propietario(propietario_id: int, db: Session = Depends(get_db)):
    return PropietarioService.eliminar_propietario(db, propietario_id)
