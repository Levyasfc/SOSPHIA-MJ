from sqlalchemy.orm import Session
from fastapi import HTTPException, BackgroundTasks, status
from app import models, schemas
from app.common.Utilidades.clientes import obtener_usuario_externo
from app.utilidades.correos import enviar_email
from app.common.plantillas.poder import mensaje_poder_otorgado


class PoderService:

    @staticmethod
    async def crear_poder(
        db: Session,
        data: schemas.PoderCreate,
        hp_id: int,
        otorgante_email: str,
        background_tasks: BackgroundTasks
    ):

        usuarios = await obtener_usuario_externo(hp_id)

        if not isinstance(usuarios, list):
            raise HTTPException(500, "Error al obtener usuarios de la PH")

        otorgante = next((u for u in usuarios if u["email"] == otorgante_email), None)

        if not otorgante:
            raise HTTPException(403, "El propietario no pertenece a esta PH")

        if otorgante["role"] != "PROPIETARIO TITULAR":
            raise HTTPException(403, "Solo un propietario titular puede otorgar un poder")

        apoderado = next((u for u in usuarios if u["user_id"] == data.apoderado_id), None)

        if not apoderado:
            raise HTTPException(404, "El apoderado no pertenece a la PH")

        poder = models.Poder(
            hp_id=hp_id,
            otorgante_id=otorgante["user_id"],
            apoderado_id=apoderado["user_id"],
            fecha_otorgado=data.fecha_otorgado,
            fecha_expiracion=data.fecha_expiracion
        )

        db.add(poder)
        db.commit()
        db.refresh(poder)

        mensaje = mensaje_poder_otorgado(
            otorgante=otorgante,
            apoderado=apoderado,
            poder=poder
        )

        background_tasks.add_task(
            enviar_email,
            apoderado["email"],
            "📄 Nuevo Poder Otorgado",
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
            raise HTTPException(404, "Poder no encontrado")

        db.delete(poder)
        db.commit()

        return {"message": "Poder eliminado correctamente"}
