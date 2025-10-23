from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.database import get_db
from app import models, schemas

router = APIRouter(
    prefix="/comunicaciones",
    tags=["Comunicaciones de Cobro"]
)

# Crear comunicación
@router.post("/", response_model=schemas.ComunicacionCobro)
def crear_comunicacion(comunicacion: schemas.ComunicacionCobroCreate, db: Session = Depends(get_db)):
    # Verificar propietario
    propietario = db.query(models.Propietario).filter(models.Propietario.id == comunicacion.propietario_id).first()
    if not propietario:
        raise HTTPException(status_code=404, detail="Propietario no encontrado")

    # Verificar deuda
    deuda = db.query(models.Deuda).filter(models.Deuda.id == comunicacion.deuda_id).first()
    if not deuda:
        raise HTTPException(status_code=404, detail="Deuda no encontrada")

    # Crear comunicación
    db_com = models.ComunicacionCobro(
        propietario_id=comunicacion.propietario_id,
        deuda_id=comunicacion.deuda_id,
        medio=comunicacion.medio,
        mensaje=comunicacion.mensaje,
        recibido=comunicacion.recibido,
        autorizado_contacto=comunicacion.autorizado_contacto,
        fecha_envio=datetime.utcnow()
    )
    db.add(db_com)
    db.commit()
    db.refresh(db_com)
    return db_com

# Listar todas
@router.get("/", response_model=List[schemas.ComunicacionCobro])
def listar_comunicaciones(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.ComunicacionCobro).offset(skip).limit(limit).all()

# Obtener por ID
@router.get("/{com_id}", response_model=schemas.ComunicacionCobro)
def obtener_comunicacion(com_id: int, db: Session = Depends(get_db)):
    com = db.query(models.ComunicacionCobro).filter(models.ComunicacionCobro.id == com_id).first()
    if not com:
        raise HTTPException(status_code=404, detail="Comunicación no encontrada")
    return com

# Actualizar comunicación
@router.put("/{com_id}", response_model=schemas.ComunicacionCobro)
def actualizar_comunicacion(com_id: int, update: schemas.ComunicacionCobroUpdate, db: Session = Depends(get_db)):
    com = db.query(models.ComunicacionCobro).filter(models.ComunicacionCobro.id == com_id).first()
    if not com:
        raise HTTPException(status_code=404, detail="Comunicación no encontrada")

    for key, value in update.dict(exclude_unset=True).items():
        setattr(com, key, value)

    db.commit()
    db.refresh(com)
    return com

# Eliminar comunicación
@router.delete("/{com_id}", response_model=schemas.ComunicacionCobro)
def eliminar_comunicacion(com_id: int, db: Session = Depends(get_db)):
    com = db.query(models.ComunicacionCobro).filter(models.ComunicacionCobro.id == com_id).first()
    if not com:
        raise HTTPException(status_code=404, detail="Comunicación no encontrada")

    db.delete(com)
    db.commit()
    return com