from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime

from app import models, schemas


class DeudasService:

    @staticmethod
    def crear_deuda(db: Session, data: schemas.DeudaCreate):
        # Validar propietario
        propietario = db.query(models.Propietario).filter_by(id=data.propietario_id).first()
        if not propietario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="El propietario no existe"
            )

        if data.valor_original <= 0:
            raise HTTPException(status_code=400, detail="El valor debe ser mayor a 0")

        # Calcular valor total inicial
        valor_total = data.valor_original + (data.interes_mora or 0)

        nueva_deuda = models.Deuda(
            propietario_id=data.propietario_id,
            descripcion=data.descripcion,
            valor_original=data.valor_original,
            interes_mora=data.interes_mora or 0,
            valor_total=valor_total,
            fecha_vencimiento=data.fecha_vencimiento,
            pagado=False
        )

        db.add(nueva_deuda)
        db.commit()
        db.refresh(nueva_deuda)
        return nueva_deuda

    @staticmethod
    def obtener_deudas(db: Session):
        return db.query(models.Deuda).all()

    @staticmethod
    def obtener_deuda(db: Session, deuda_id: int):
        deuda = db.query(models.Deuda).filter_by(id=deuda_id).first()
        if not deuda:
            raise HTTPException(status_code=404, detail="Deuda no encontrada")
        return deuda

    @staticmethod
    def actualizar_deuda(db: Session, deuda_id: int, data: schemas.DeudaUpdate):
        deuda = db.query(models.Deuda).filter_by(id=deuda_id).first()
        if not deuda:
            raise HTTPException(status_code=404, detail="Deuda no encontrada")

        # Evitar modificar después de pagar
        if deuda.pagado:
            raise HTTPException(status_code=400, detail="La deuda ya está pagada y no puede ser editada")

        deuda.descripcion = data.descripcion or deuda.descripcion
        deuda.interes_mora = data.interes_mora if data.interes_mora is not None else deuda.interes_mora
        deuda.valor_original = data.valor_original or deuda.valor_original

        # Recalcular total
        deuda.valor_total = deuda.valor_original + deuda.interes_mora

        # Pago
        if data.pagado is True and not deuda.pagado:
            deuda.pagado = True
            deuda.fecha_pago = datetime.utcnow()

        db.commit()
        db.refresh(deuda)
        return deuda

    @staticmethod
    def eliminar_deuda(db: Session, deuda_id: int):
        deuda = db.query(models.Deuda).filter_by(id=deuda_id).first()
        if not deuda:
            raise HTTPException(status_code=404, detail="Deuda no encontrada")

        db.delete(deuda)
        db.commit()
        return {"message": "Deuda eliminada exitosamente"}
