from app import models, schemas
from fastapi import HTTPException, BackgroundTasks
from sqlalchemy.orm import Session

from app.utilidades.correos import enviar_email
from app.common.plantillas.usuario import mensaje_nuevo_propietario

class PropietarioService:

    @staticmethod
    def crear_propietario(db: Session, data: schemas.PropietarioCreate, background_tasks: BackgroundTasks):
        propietario = models.Propietario(**data.dict())
        db.add(propietario)
        db.commit()
        db.refresh(propietario)

        if propietario.correo and propietario.autorizacion_datos:
            asunto = "✅ Registro exitoso en la SOSPHIA!!"
            mensaje = mensaje_nuevo_propietario(propietario)
            background_tasks.add_task(enviar_email, propietario.correo, asunto, mensaje)

        return propietario

    @staticmethod
    def obtener_propietario(db: Session, propietario_id: int):
        propietario = db.query(models.Propietario).filter(models.Propietario.id == propietario_id).first()
        if not propietario:
            raise HTTPException(status_code=404, detail="Propietario no encontrado")
        return propietario

    @staticmethod
    def obtener_propietarios(db: Session):
        return db.query(models.Propietario).all()

    @staticmethod
    def actualizar_propietario(db: Session, propietario_id: int, data: schemas.PropietarioUpdate):
        propietario = PropietarioService.obtener_propietario(db, propietario_id)
        for key, value in data.dict(exclude_unset=True).items():
            setattr(propietario, key, value)
        db.commit()
        db.refresh(propietario)
        return propietario

    @staticmethod
    def eliminar_propietario(db: Session, propietario_id: int):
        propietario = PropietarioService.obtener_propietario(db, propietario_id)
        db.delete(propietario)
        db.commit()
        return {"msg": "Propietario eliminado correctamente"}
