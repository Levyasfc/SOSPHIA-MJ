from sqlalchemy.orm import Session
from fastapi import HTTPException, BackgroundTasks
from datetime import datetime

from app import models, schemas
from app.utilidades.correos import enviar_email
from app.common.plantillas.asamblea import mensaje_nueva_asamblea
from app.common.Utilidades.clientes import obtener_usuario_externo
from app.common.Utilidades.permisos import validar_rol, validar_pertenencia_ph


class AsambleaService:

    @staticmethod
    async def crear_asamblea(
        db: Session,
        hp_id: int,
        data: schemas.AsambleaCreate,
        usuario: dict,
        background_tasks: BackgroundTasks
    ):
        
        validar_pertenencia_ph(usuario, hp_id)

        validar_rol(usuario, ["ADMINISTRADOR", "ADMINISTRADOR INMOBILIARIO"])

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

        usuarios = await obtener_usuario_externo(hp_id)
        if not usuarios:
            return asamblea  

        correos = [u["email"] for u in usuarios if u.get("email")]

        if correos:
            asunto = f"📢 Nueva Asamblea: {asamblea.tipo}"
            mensaje = mensaje_nueva_asamblea(asamblea)

            for email in correos:
                background_tasks.add_task(enviar_email, email, asunto, mensaje)

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
