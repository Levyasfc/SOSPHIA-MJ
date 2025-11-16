from sqlalchemy.orm import Session
from fastapi import HTTPException, status, BackgroundTasks
from app import models, schemas
from app.common.plantillas.poder import mensaje_poder_otorgado
from app.utilidades.correos import enviar_email
from app.common.Utilidades.clientes import obtener_usuario_externo


class PoderService:

    @staticmethod
    async def crear_poder(db: Session, data: schemas.PoderCreate, hp_id: int, background_tasks: BackgroundTasks):

        # Obtener usuarios externos de la HP
        usuarios = await obtener_usuario_externo(hp_id)

        if not isinstance(usuarios, list):
            usuarios = []

        # Buscar otorgante y apoderado por user_id
        otorgante = next((u for u in usuarios if u["user_id"] == data.otorgante_id), None)
        apoderado = next((u for u in usuarios if u["user_id"] == data.apoderado_id), None)

        if not otorgante or not apoderado:
            raise HTTPException(status_code=404, detail="Otorgante o apoderado no encontrado en la HP")

        # Crear el poder
        poder = models.Poder(
            hp_id=hp_id,
            otorgante_id=data.otorgante_id,
            apoderado_id=data.apoderado_id,
            fecha_otorgado=data.fecha_otorgado,
            fecha_expiracion=data.fecha_expiracion
        )

        db.add(poder)
        db.commit()
        db.refresh(poder)

        # Enviar correo al apoderado
        correo = apoderado.get("email")

        if correo:
            mensaje = mensaje_poder_otorgado(
                otorgante=otorgante,
                apoderado=apoderado,
                poder=poder
            )

            background_tasks.add_task(
                enviar_email,
                correo,
                "📄 Nuevo poder asignado",
                mensaje
            )

        return poder

    @staticmethod
    def obtener_poderes(db: Session, hp_id: int):
        return db.query(models.Poder).filter_by(hp_id=hp_id).all()

    @staticmethod
    def eliminar_poder(db: Session, poder_id: int, hp_id: int):
        poder = db.query(models.Poder).filter_by(id=poder_id, hp_id=hp_id).first()
        if not poder:
            raise HTTPException(status_code=404, detail="Poder no encontrado")

        db.delete(poder)
        db.commit()
        return {"msg": "Poder eliminado correctamente"}