from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app import models, schemas
from datetime import datetime

class AsambleaService:

    @staticmethod
    def crear_asamblea(db: Session, data: schemas.AsambleaCreate):
        asamblea = models.Asamblea(
            fecha=data.fecha or datetime.utcnow(),
            tipo=data.tipo,
            descripcion=data.descripcion,
            lugar=data.lugar
        )
        db.add(asamblea)
        db.commit()
        db.refresh(asamblea)
        return asamblea

    @staticmethod
    def obtener_asambleas(db: Session):
        return db.query(models.Asamblea).all()

    @staticmethod
    def obtener_asamblea(db: Session, asamblea_id: int):
        a = db.query(models.Asamblea).filter_by(id=asamblea_id).first()
        if not a:
            raise HTTPException(status_code=404, detail="Asamblea no encontrada")
        return a
