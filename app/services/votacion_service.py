from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app import models, schemas

class VotacionService:
    @staticmethod
    def crear_votacion(db: Session, data: schemas.VotacionCreate):
        asamblea = db.query(models.Asamblea).filter_by(id=data.asamblea_id).first()
        if not asamblea:
            raise HTTPException(status_code=404, detail="Asamblea no encontrada")
        vot = models.Votacion(
            asamblea_id=data.asamblea_id,
            propuesta=data.propuesta
        )
        db.add(vot)
        db.commit()
        db.refresh(vot)
        return vot

    @staticmethod
    def votar(db: Session, votacion_id: int, favor: int = 0, contra: int = 0, abstencion: int = 0):
        v = db.query(models.Votacion).filter_by(id=votacion_id).first()
        if not v:
            raise HTTPException(status_code=404, detail="Votación no encontrada")
        v.votos_favor += favor
        v.votos_contra += contra
        v.abstenciones += abstencion

        # calcular resultado simple
        if v.votos_favor > v.votos_contra:
            v.resultado = "Aprobado"
        elif v.votos_contra > v.votos_favor:
            v.resultado = "Rechazado"
        else:
            v.resultado = "Empate"

        db.commit()
        db.refresh(v)
        return v

    @staticmethod
    def obtener_votaciones(db: Session):
        return db.query(models.Votacion).all()
