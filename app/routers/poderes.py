from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.database import get_db
from app import models, schemas

router = APIRouter(
    prefix="/poderes",
    tags=["PoderesVotaciones"]
)

# Crear poder/votación
@router.post("/", response_model=schemas.PoderVotacion)
def crear_poder(poder: schemas.PoderVotacionCreate, db: Session = Depends(get_db)):
    # Verificar que el propietario exista
    propietario = db.query(models.Propietario).filter(models.Propietario.id == poder.propietario_id).first()
    if not propietario:
        raise HTTPException(status_code=404, detail="Propietario no encontrado")

    db_poder = models.PoderVotacion(**poder.dict())
    if not db_poder.fecha_votacion:
        db_poder.fecha_votacion = datetime.utcnow()
    db.add(db_poder)
    db.commit()
    db.refresh(db_poder)
    return db_poder

# Listar todos los poderes/votaciones
@router.get("/", response_model=List[schemas.PoderVotacion])
def listar_poderes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.PoderVotacion).offset(skip).limit(limit).all()

# Obtener poder/votación por ID
@router.get("/{poder_id}", response_model=schemas.PoderVotacion)
def obtener_poder(poder_id: int, db: Session = Depends(get_db)):
    poder = db.query(models.PoderVotacion).filter(models.PoderVotacion.id == poder_id).first()
    if not poder:
        raise HTTPException(status_code=404, detail="Poder/Votación no encontrado")
    return poder

# Actualizar poder/votación
@router.put("/{poder_id}", response_model=schemas.PoderVotacion)
def actualizar_poder(poder_id: int, update: schemas.PoderVotacionCreate, db: Session = Depends(get_db)):
    poder = db.query(models.PoderVotacion).filter(models.PoderVotacion.id == poder_id).first()
    if not poder:
        raise HTTPException(status_code=404, detail="Poder/Votación no encontrado")
    
    for key, value in update.dict(exclude_unset=True).items():
        setattr(poder, key, value)
    
    db.commit()
    db.refresh(poder)
    return poder

# Eliminar poder/votación
@router.delete("/{poder_id}", response_model=schemas.PoderVotacion)
def eliminar_poder(poder_id: int, db: Session = Depends(get_db)):
    poder = db.query(models.PoderVotacion).filter(models.PoderVotacion.id == poder_id).first()
    if not poder:
        raise HTTPException(status_code=404, detail="Poder/Votación no encontrado")
    
    db.delete(poder)
    db.commit()
    return poder