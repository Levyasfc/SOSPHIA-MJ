from sqlalchemy.orm import Session
from fastapi import HTTPException, BackgroundTasks
from datetime import datetime

from app import models, schemas
from app.utilidades.correos import enviar_email
from app.common.plantillas.juridico import (
    correo_nuevo_caso,
    correo_nuevo_historial,
    correo_estado_actualizado
)
from app.common.Utilidades.clientes import obtener_usuario_externo


class CasosJuridicosService:

    @staticmethod
    async def crear_caso(db: Session, data: schemas.CasoJuridicoCreate, hp_id: int, user_id: int, background_tasks: BackgroundTasks):

        usuario_data = await obtener_usuario_externo(hp_id)

        usuario_nombre = "Usuario Desconocido"
        if isinstance(usuario_data, list):
            u = next((x for x in usuario_data if x.get("user_id") == user_id), None)
            if u:
                usuario_nombre = f"{u['person']['first_name']} {u['person']['last_name']}"

        caso = models.CasoJuridico(
            hp_id=hp_id,
            titulo=data.titulo,
            descripcion=data.descripcion,
            estado="Abierto",
            usuario_creador=user_id,
            fecha_creacion=datetime.utcnow()
        )

        db.add(caso)
        db.commit()
        db.refresh(caso)

        # Notificación por correo
        email_admin = "admin@sophia.com"  # ← cámbialo si quieres
        mensaje = correo_nuevo_caso(caso, usuario_nombre)

        background_tasks.add_task(enviar_email, email_admin, "📄 Nuevo Caso Jurídico", mensaje)

        return caso


    @staticmethod
    async def agregar_historial(db: Session, caso_id: int, hp_id: int, data: schemas.HistorialJuridicoCreate, user_id: int, background_tasks: BackgroundTasks):

        caso = db.query(models.CasoJuridico).filter_by(id=caso_id, hp_id=hp_id).first()
        if not caso:
            raise HTTPException(status_code=404, detail="Caso no encontrado")

        usuario_data = await obtener_usuario_externo(hp_id)

        usuario_nombre = "Usuario"
        email_destino = None

        if isinstance(usuario_data, list):
            u = next((x for x in usuario_data if x.get("user_id") == user_id), None)
            if u:
                usuario_nombre = f"{u['person']['first_name']} {u['person']['last_name']}"
                email_destino = u.get("email")

        historial = models.HistorialJuridico(
            caso_id=caso_id,
            descripcion=data.descripcion,
            usuario=usuario_nombre,
            fecha=datetime.utcnow()
        )

        db.add(historial)
        db.commit()
        db.refresh(historial)

        # Notificación
        if email_destino:
            mensaje = correo_nuevo_historial(caso, historial)
            background_tasks.add_task(
                enviar_email, email_destino,
                f"📌 Actualización del caso: {caso.titulo}",
                mensaje
            )

        return historial
    
    @staticmethod
    def cambiar_estado(db: Session, caso_id: int, hp_id: int, nuevo_estado: str, background_tasks: BackgroundTasks):

        caso = db.query(models.CasoJuridico).filter_by(id=caso_id, hp_id=hp_id).first()
        if not caso:
            raise HTTPException(status_code=404, detail="Caso no encontrado")

        caso.estado = nuevo_estado
        db.commit()
        db.refresh(caso)

        mensaje = correo_estado_actualizado(caso, nuevo_estado)

        return caso

    @staticmethod
    def obtener_casos(db: Session, hp_id: int):
        return db.query(models.CasoJuridico).filter_by(hp_id=hp_id).all()


    @staticmethod
    def obtener_caso(db: Session, caso_id: int, hp_id: int):
        caso = db.query(models.CasoJuridico).filter_by(id=caso_id, hp_id=hp_id).first()
        if not caso:
            raise HTTPException(status_code=404, detail="Caso no encontrado")
        return caso


    @staticmethod
    async def agregar_historial(db: Session, caso_id: int, hp_id: int, data: schemas.HistorialJuridicoCreate, user_id: int):

        caso = db.query(models.CasoJuridico).filter_by(id=caso_id, hp_id=hp_id).first()
        if not caso:
            raise HTTPException(status_code=404, detail="Caso no encontrado")

        usuario = await obtener_usuario_externo(user_id)
        nombre_usuario = (
            f"{usuario.get('person', {}).get('first_name', '')} "
            f"{usuario.get('person', {}).get('last_name', '')}"
        ).strip()

        historial = models.HistorialJuridico(
            caso_id=caso_id,
            descripcion=data.descripcion,
            usuario=nombre_usuario
        )

        db.add(historial)
        db.commit()
        db.refresh(historial)

        return historial


    @staticmethod
    def cambiar_estado(db: Session, caso_id: int, hp_id: int, nuevo_estado: str):

        caso = db.query(models.CasoJuridico).filter_by(id=caso_id, hp_id=hp_id).first()
        if not caso:
            raise HTTPException(status_code=404, detail="Caso no encontrado")

        caso.estado = nuevo_estado
        db.commit()
        db.refresh(caso)

        return caso
