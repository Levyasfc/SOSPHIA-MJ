from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Union
from datetime import datetime

from app.database import get_db
from app import models, schemas

router = APIRouter(
    prefix="/deudas",
    tags=["Deudas"]
)

# Crear deuda
@router.post("/", response_model=schemas.Deuda)
def crear_deuda(deuda: schemas.DeudaCreate, db: Session = Depends(get_db)):
    # Verificar que el propietario exista
    propietario = db.query(models.Propietario).filter(models.Propietario.id == deuda.propietario_id).first()
    if not propietario:
        raise HTTPException(status_code=404, detail="Propietario no encontrado")

    # Crear deuda usando todos los campos del schema
    db_deuda = models.Deuda(**deuda.dict())
    db.add(db_deuda)
    db.commit()
    db.refresh(db_deuda)
    return db_deuda

# Listar deudas
@router.get("/", response_model=List[schemas.Deuda])
def listar_deudas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Deuda).offset(skip).limit(limit).all()

# Obtener deuda por ID
@router.get("/{deuda_id}", response_model=schemas.Deuda)
def obtener_deuda(deuda_id: int, db: Session = Depends(get_db)):
    deuda = db.query(models.Deuda).filter(models.Deuda.id == deuda_id).first()
    if not deuda:
        raise HTTPException(status_code=404, detail="Deuda no encontrada")
    return deuda

@router.get("/propietario/{propietario_id}", response_model=Union[List[schemas.Deuda], dict])
def obtener_deudas_por_propietario(propietario_id: int, db: Session = Depends(get_db)):
    # Verificar si el propietario existe
    propietario = db.query(models.Propietario).filter(models.Propietario.id == propietario_id).first()
    if not propietario:
        raise HTTPException(status_code=404, detail="Propietario no encontrado")

    # Obtener las deudas del propietario
    deudas = db.query(models.Deuda).filter(models.Deuda.propietario_id == propietario_id).all()

    if not deudas:
        # Retornar un mensaje en lugar de lista vacía
        return {"mensaje": "El propietario no tiene deudas"}

    return deudas


# Actualizar deuda
@router.put("/{deuda_id}", response_model=schemas.Deuda)
def actualizar_deuda(deuda_id: int, update: schemas.DeudaUpdate, db: Session = Depends(get_db)):
    deuda = db.query(models.Deuda).filter(models.Deuda.id == deuda_id).first()
    if not deuda:
        raise HTTPException(status_code=404, detail="Deuda no encontrada")
    for key, value in update.dict(exclude_unset=True).items():
        setattr(deuda, key, value)
    db.commit()
    db.refresh(deuda)
    return deuda

# Eliminar deuda
@router.delete("/{deuda_id}", response_model=schemas.Deuda)
def eliminar_deuda(deuda_id: int, db: Session = Depends(get_db)):
    deuda = db.query(models.Deuda).filter(models.Deuda.id == deuda_id).first()
    if not deuda:
        raise HTTPException(status_code=404, detail="Deuda no encontrada")
    db.delete(deuda)
    db.commit()
    return deuda
