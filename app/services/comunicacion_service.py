from datetime import datetime, timedelta
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app import models, schemas


class ComunicacionService:

    @staticmethod
    def crear_comunicacion(db: Session, data: schemas.ComunicacionCobroCreate):
        # Validar que la deuda exista
        deuda = db.query(models.Deuda).filter(models.Deuda.id == data.deuda_id).first()
        if not deuda:
            raise HTTPException(status_code=404, detail="La deuda no existe")

        # Validar que pertenece al propietario
        if deuda.propietario_id != data.propietario_id:
            raise HTTPException(status_code=400, detail="La deuda no pertenece al propietario")

        # Verificar autorización de contacto
        propietario = db.query(models.Propietario).filter(models.Propietario.id == data.propietario_id).first()
        if not propietario.autorizado_contacto:
            raise HTTPException(status_code=403, detail="El propietario no autorizó contacto")

        # Evitar spam — 1 comunicación por día
        ultima = (
            db.query(models.ComunicacionCobro)
            .filter(models.ComunicacionCobro.deuda_id == data.deuda_id)
            .order_by(models.ComunicacionCobro.fecha_envio.desc())
            .first()
        )

        if ultima and ultima.fecha_envio > datetime.utcnow() - timedelta(hours=24):
            raise HTTPException(status_code=429, detail="Solo se permite una comunicación cada 24 horas")

        nueva = models.ComunicacionCobro(
            propietario_id=data.propietario_id,
            deuda_id=data.deuda_id,
            medio=data.medio,
            mensaje=data.mensaje,
            recibido=data.recibido,
            autorizado_contacto=True,
        )

        db.add(nueva)
        db.commit()
        db.refresh(nueva)
        return nueva


    @staticmethod
    def obtener_comunicaciones(db: Session):
        return db.query(models.ComunicacionCobro).all()


    @staticmethod
    def obtener_historial_por_propietario(db: Session, propietario_id: int):
        return (
            db.query(models.ComunicacionCobro)
            .filter(models.ComunicacionCobro.propietario_id == propietario_id)
            .all()
        )


    @staticmethod
    def obtener_historial_por_deuda(db: Session, deuda_id: int):
        return (
            db.query(models.ComunicacionCobro)
            .filter(models.ComunicacionCobro.deuda_id == deuda_id)
            .all()
        )
