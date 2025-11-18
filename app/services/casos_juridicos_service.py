from sqlalchemy.orm import Session
from fastapi import HTTPException, BackgroundTasks
from datetime import datetime

from app import models, schemas
from app.utilidades.correos import enviar_email


class CasosJuridicosService:

    @staticmethod
    async def crear_caso(db: Session, data: schemas.CasoJuridicoCreate, hp_id: int, user_id: int, background_tasks: BackgroundTasks):

        caso = models.CasoJuridico(
            hp_id=hp_id,
            titulo=data.titulo,
            descripcion=data.descripcion,
            usuario_creador=user_id,
            fecha_creacion=datetime.utcnow()
        )

        db.add(caso)
        db.commit()
        db.refresh(caso)

        # Enviar correo opcional
        if data.notificar:
            asunto = f"📄 Nuevo Caso Jurídico: {caso.titulo}"
            mensaje = f"Se ha creado un nuevo caso jurídico.\n\nTítulo: {caso.titulo}\nDescripción: {caso.descripcion}"
            background_tasks.add_task(enviar_email, data.correo_responsable, asunto, mensaje)

        return caso


    @staticmethod
    def obtener_casos(db: Session, hp_id: int):
        return db.query(models.CasoJuridico).filter_by(hp_id=hp_id).all()


    @staticmethod
    def obtener_caso(db: Session, caso_id: int, hp_id: int):
        caso = db.query(models.CasoJuridico).filter_by(id=caso_id, hp_id=hp_id).first()

        if not caso:
            raise HTTPException(status_code=404, detail="Caso jurídico no encontrado")

        return caso


    @staticmethod
    async def agregar_historial(db: Session, caso_id: int, hp_id: int, data: schemas.HistorialJuridicoCreate, background_tasks: BackgroundTasks):

        caso = db.query(models.CasoJuridico).filter_by(id=caso_id, hp_id=hp_id).first()
        if not caso:
            raise HTTPException(status_code=404, detail="Caso jurídico no encontrado")

        historial = models.HistorialJuridico(
            caso_id=caso.id,
            descripcion=data.descripcion,
            usuario=data.usuario,
            fecha=datetime.utcnow()
        )

        db.add(historial)
        db.commit()
        db.refresh(historial)

        # Notificar por correo
        if data.notificar:
            asunto = f"📌 Actualización en Caso Jurídico: {caso.titulo}"
            mensaje = f"Se agregó un historial:\n\n{data.descripcion}"
            background_tasks.add_task(enviar_email, data.correo_responsable, asunto, mensaje)

        return historial
