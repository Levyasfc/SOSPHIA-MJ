from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.propietario_schema import PropietarioCreate, PropietarioResponse
from app.models.propietario import Propietario
from typing import List

router = APIRouter(prefix="/propietarios", tags=["Propietarios"])

@router.post("/", response_model=PropietarioResponse, status_code=status.HTTP_201_CREATED)
def crear_propietario(payload: PropietarioCreate, db: Session = Depends(get_db)):
    nuevo = Propietario(**payload.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@router.get("/", response_model=List[PropietarioResponse])
def listar_propietarios(db: Session = Depends(get_db)):
    return db.query(Propietario).all()

@router.get("/{propietario_id}", response_model=PropietarioResponse)
def obtener_propietario(propietario_id: int, db: Session = Depends(get_db)):
    p = db.query(Propietario).filter(Propietario.id == propietario_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Propietario no encontrado")
    return p
