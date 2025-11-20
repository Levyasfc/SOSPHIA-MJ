from sqlalchemy.orm import Session
from fastapi import HTTPException, BackgroundTasks
from datetime import datetime

from app import models, schemas
from app.utilidades.correos import enviar_email
from app.common.Utilidades.permisos import validar_pertenencia_ph, validar_rol


class CasosJuridicosService:

    @staticmethod
    async def crear_caso(
        db: Session,
        data: schemas.CasoJuridicoCreate,
        hp_id: int,
        user_id: int,
        background_tasks: BackgroundTasks
    ):
        deuda = db.query(models.Deuda).filter_by(id=data.deuda_id, hp_id=hp_id).first()
        if not deuda:
            raise HTTPException(status_code=404, detail="La deuda no existe o no pertenece a esta PH")

        caso = models.CasoJuridico(
            hp_id=hp_id,
            deuda_id=data.deuda_id,
            estado="En revisión",
            motivo=data.motivo,
            abogado=None,
            fecha_inicio=datetime.utcnow()
        )

        db.add(caso)
        db.commit()
        db.refresh(caso)

        if data.notificar and data.correo_responsable:
            asunto = f"📄 Nuevo Caso Jurídico creado"
            mensaje = (
                f"Se ha creado un nuevo caso jurídico.\n\n"
                f"Deuda asociada ID: {data.deuda_id}\n"
                f"Motivo: {data.motivo}\n"
            )
            background_tasks.add_task(enviar_email, data.correo_responsable, asunto, mensaje)

        return caso

    @staticmethod
    def obtener_casos(db: Session, hp_id: int):
        return db.query(models.CasoJuridico).filter_by(hp_id=hp_id).all()

    # Solo para propietarios
    @staticmethod
    def obtener_casos_por_usuario(db: Session, hp_id: int, user_id: int):
        return (
            db.query(models.CasoJuridico)
            .join(models.Deuda, models.Deuda.id == models.CasoJuridico.deuda_id)
            .filter(models.Deuda.propietario_id == user_id)
            .filter(models.CasoJuridico.hp_id == hp_id)
            .all()
        )

    @staticmethod
    def obtener_caso(db: Session, caso_id: int, hp_id: int):
        caso = db.query(models.CasoJuridico).filter_by(id=caso_id, hp_id=hp_id).first()

        if not caso:
            raise HTTPException(status_code=404, detail="Caso jurídico no encontrado")

        return caso


    @staticmethod
    async def agregar_historial(
        db: Session,
        caso_id: int,
        hp_id: int,
        data: schemas.HistorialJuridicoCreate,
        correo_usuario: str,
        background_tasks: BackgroundTasks
    ):
        caso = db.query(models.CasoJuridico).filter_by(id=caso_id, hp_id=hp_id).first()
        if not caso:
            raise HTTPException(status_code=404, detail="Caso jurídico no encontrado")

        historial = models.HistorialJuridico(
            caso_id=caso.id,
            descripcion=data.descripcion,
            usuario=correo_usuario,
            fecha=datetime.utcnow()
        )

        db.add(historial)
        db.commit()
        db.refresh(historial)

        if data.notificar and data.correo_responsable:
            asunto = f"📌 Actualización en Caso Jurídico"
            mensaje = f"Se agregó una actualización:\n\n{data.descripcion}"
            background_tasks.add_task(enviar_email, data.correo_responsable, asunto, mensaje)

        return historial
    
    @staticmethod
    async def tomar_caso(
        db: Session,
        hp_id: int,
        caso_id: int,
        abogado_email: str
    ):
        caso = db.query(models.CasoJuridico).filter_by(
            id=caso_id,
            hp_id=hp_id
        ).first()

        if not caso:
            raise HTTPException(status_code=404, detail="Caso jurídico no encontrado")

        if caso.abogado:
            raise HTTPException(
                status_code=400,
                detail=f"El caso ya fue tomado por: {caso.abogado}"
            )

        caso.abogado = abogado_email
        caso.estado = "En gestión"

        db.commit()
        db.refresh(caso)

        return caso


    @staticmethod
    async def cerrar_caso(
        db: Session,
        hp_id: int,
        caso_id: int,
        abogado_email: str
    ):
        caso = db.query(models.CasoJuridico).filter_by(
            id=caso_id,
            hp_id=hp_id
        ).first()

        if not caso:
            raise HTTPException(status_code=404, detail="Caso jurídico no encontrado")

        # Validar que no esté ya cerrado
        if caso.fecha_cierre is not None:
            raise HTTPException(
                status_code=400,
                detail="El caso ya se encuentra cerrado"
            )

        # Validar que tenga abogado asignado
        if not caso.abogado:
            raise HTTPException(
                status_code=400,
                detail="No se puede cerrar un caso sin un abogado asignado"
            )

        # Cambiar estado y asignar fecha de cierre
        caso.estado = "Cerrado"
        caso.fecha_cierre = datetime.utcnow()

        db.commit()
        db.refresh(caso)

        return caso