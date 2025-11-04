from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app import models, schemas

class PoderService:

    @staticmethod
    def crear_poder(db: Session, data: schemas.PoderCreate):
        # Validar propietarios
        otorgante = db.query(models.Propietario).filter_by(id=data.otorgante_id).first()
        apoderado = db.query(models.Propietario).filter_by(id=data.apoderado_id).first()
        if not otorgante or not apoderado:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Otorgante o apoderado no existe")

        poder = models.Poder(
            otorgante_id=data.otorgante_id,
            apoderado_id=data.apoderado_id,
            fecha_otorgado=data.fecha_otorgado,
            fecha_expiracion=data.fecha_expiracion
        )
        db.add(poder)
        db.commit()
        db.refresh(poder)
        return poder

    @staticmethod
    def obtener_poderes(db: Session):
        return db.query(models.Poder).all()

    @staticmethod
    def eliminar_poder(db: Session, poder_id: int):
        poder = db.query(models.Poder).filter_by(id=poder_id).first()
        if not poder:
            raise HTTPException(status_code=404, detail="Poder no encontrado")
        db.delete(poder)
        db.commit()
        return {"msg": "Poder eliminado"}
