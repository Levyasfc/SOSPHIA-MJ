from sqlalchemy.orm import Session
from fastapi import HTTPException, BackgroundTasks
from app import models, schemas
from app.utilidades.correos import enviar_email
from app.common.plantillas.votacion import mensaje_confirmacion_voto
from app.common.Utilidades.clientes import obtener_usuario_externo


class VotacionService:

    @staticmethod
    def crear_votacion(db: Session, data: schemas.VotacionCreate, hp_id: int):
        asamblea = db.query(models.Asamblea).filter_by(id=data.asamblea_id, hp_id=hp_id).first()
        if not asamblea:
            raise HTTPException(status_code=404, detail="Asamblea no encontrada en esta PH")

        vot = models.Votacion(
            hp_id=hp_id,
            asamblea_id=data.asamblea_id,
            propuesta=data.propuesta
        )
        db.add(vot)
        db.commit()
        db.refresh(vot)
        return vot

    def votar(db: Session, votacion_id: int, hp_id: int, usuario_id: int, voto: str):

        v = db.query(models.Votacion).filter_by(
            id=votacion_id,
            hp_id=hp_id
        ).first()

        if not v:
            raise HTTPException(404, "Votación no encontrada en esta PH")

        voto_existente = db.query(models.Voto).filter_by(
            votacion_id=votacion_id,
            usuario_id=usuario_id
        ).first()

        if voto_existente:
            raise HTTPException(400, "Ya has votado en esta votación")

        # 3️⃣ Registrar voto
        nuevo_voto = models.Voto(
            hp_id=hp_id,
            votacion_id=votacion_id,
            usuario_id=usuario_id,
            voto=voto
        )
        db.add(nuevo_voto)

        if voto == "FAVOR":
            v.votos_favor += 1
        elif voto == "CONTRA":
            v.votos_contra += 1
        else:
            v.abstenciones += 1

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
    def obtener_votaciones(db: Session, hp_id: int):
        return db.query(models.Votacion).filter_by(hp_id=hp_id).all()
