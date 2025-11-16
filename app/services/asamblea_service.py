from sqlalchemy.orm import Session
from fastapi import HTTPException, BackgroundTasks
from datetime import datetime

from app import models, schemas
from app.utilidades.correos import enviar_email
from app.common.plantillas.asamblea import mensaje_nueva_asamblea
from app.common.Utilidades.clientes import obtener_usuario_externo


class AsambleaService:

    @staticmethod
    async def crear_asamblea(db: Session, data: schemas.AsambleaCreate, hp_id: int, background_tasks: BackgroundTasks):

        # Crear asamblea
        asamblea = models.Asamblea(
            hp_id=hp_id,
            fecha=data.fecha or datetime.utcnow(),
            tipo=data.tipo,
            descripcion=data.descripcion,
            lugar=data.lugar
        )

        db.add(asamblea)
        db.commit()
        db.refresh(asamblea)

        # Obtener usuarios de la PH
        usuarios = await obtener_usuario_externo(hp_id)

        # Filtrar SOLO usuarios con email
        emails = [u["email"] for u in usuarios if u.get("email")]

        # Enviar correos
        asunto = f"📢 Nueva Asamblea: {asamblea.tipo}"
        mensaje = mensaje_nueva_asamblea(asamblea)

        for correo in emails:
            background_tasks.add_task(enviar_email, correo, asunto, mensaje)

        return asamblea


    @staticmethod
    def obtener_asambleas(db: Session, hp_id: int):
        return db.query(models.Asamblea).filter_by(hp_id=hp_id).all()


    @staticmethod
    def obtener_asamblea(db: Session, asamblea_id: int, hp_id: int):
        a = db.query(models.Asamblea).filter_by(id=asamblea_id, hp_id=hp_id).first()
        if not a:
            raise HTTPException(status_code=404, detail="Asamblea no encontrada")
        return a
