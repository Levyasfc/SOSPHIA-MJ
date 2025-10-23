from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app import models, schemas

router = APIRouter(
    prefix="/propietarios",
    tags=["Propietarios"]
)

# Crear propietario
@router.post("/", response_model=schemas.propietario_schema.Propietario)
def crear_propietario(propietario: schemas.propietario_schema.PropietarioCreate, db: Session = Depends(get_db)):
    db_prop = models.Propietario(**propietario.dict())
    db.add(db_prop)
    db.commit()
    db.refresh(db_prop)
    return db_prop

# Listar todos los propietarios
@router.get("/", response_model=List[schemas.Propietario])
def listar_propietarios(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Propietario).offset(skip).limit(limit).all()

# Obtener propietario por ID
@router.get("/{propietario_id}", response_model=schemas.Propietario)
def obtener_propietario(propietario_id: int, db: Session = Depends(get_db)):
    db_prop = db.query(models.Propietario).filter(models.Propietario.id == propietario_id).first()
    if not db_prop:
        raise HTTPException(status_code=404, detail="Propietario no encontrado")
    return db_prop

# Actualizar propietario
@router.put("/{propietario_id}", response_model=schemas.Propietario)
def actualizar_propietario(propietario_id: int, update: schemas.PropietarioUpdate, db: Session = Depends(get_db)):
    db_prop = db.query(models.Propietario).filter(models.Propietario.id == propietario_id).first()
    if not db_prop:
        raise HTTPException(status_code=404, detail="Propietario no encontrado")
    for key, value in update.dict(exclude_unset=True).items():
        setattr(db_prop, key, value)
    db.commit()
    db.refresh(db_prop)
    return db_prop

# Eliminar propietario
@router.delete("/{propietario_id}", response_model=schemas.Propietario)
def eliminar_propietario(propietario_id: int, db: Session = Depends(get_db)):
    db_prop = db.query(models.Propietario).filter(models.Propietario.id == propietario_id).first()
    if not db_prop:
        raise HTTPException(status_code=404, detail="Propietario no encontrado")
    db.delete(db_prop)
    db.commit()
    return db_prop
