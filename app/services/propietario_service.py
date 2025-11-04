from app import models, schemas
from fastapi import HTTPException
from sqlalchemy.orm import Session

class PropietarioService:

    @staticmethod
    def crear_propietario(db: Session, data: schemas.PropietarioCreate):
        propietario = models.Propietario(**data.dict())
        db.add(propietario)
        db.commit()
        db.refresh(propietario)
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
