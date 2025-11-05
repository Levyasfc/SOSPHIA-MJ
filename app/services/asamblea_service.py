from sqlalchemy.orm import Session
from fastapi import HTTPException, BackgroundTasks
from datetime import datetime
from typing import List

from app import models, schemas
from app.utilidades.correos import enviar_email
from app.common.plantillas.asamblea import mensaje_nueva_asamblea

class AsambleaService:

    @staticmethod
    def crear_asamblea(db: Session, data: schemas.AsambleaCreate, background_tasks: BackgroundTasks):
        asamblea = models.Asamblea(
            fecha=data.fecha or datetime.utcnow(),
            tipo=data.tipo,
            descripcion=data.descripcion,
            lugar=data.lugar
        )
        db.add(asamblea)
        db.commit()
        db.refresh(asamblea)

        propietarios = db.query(models.Propietario).filter(models.Propietario.autorizacion_datos == True).all()
        emails = [p.correo for p in propietarios if p.correo]

       
        asunto = f"📢 Nueva Asamblea: {asamblea.tipo}"
        mensaje = mensaje_nueva_asamblea(asamblea)

        for email in emails:
            background_tasks.add_task(enviar_email, email, asunto, mensaje)

        return asamblea

    @staticmethod
    def obtener_asambleas(db: Session):
        return db.query(models.Asamblea).all()

    @staticmethod
    def obtener_asamblea(db: Session, asamblea_id: int):
        a = db.query(models.Asamblea).filter_by(id=asamblea_id).first()
        if not a:
            raise HTTPException(status_code=404, detail="Asamblea no encontrada")
        return a
