from sqlalchemy.orm import Session
from fastapi import BackgroundTasks, HTTPException
from app import models, schemas
from datetime import datetime
from app.utilidades.correos import enviar_email
from app.common.plantillas.deudas import mensaje_deuda

class DeudasService:

    @staticmethod
    def crear_deuda(db: Session, data: schemas.DeudaCreate, background_tasks: BackgroundTasks):
        

        hoy = datetime.datetime.now(datetime.timezone.utc).date() 
        fecha_vencimiento = data.fecha_vencimiento.date()

        valor_original = data.valor_original
        tasa_interes_mora = data.interes_mora
        valor_intereses = 0.0
        
        if hoy > fecha_vencimiento:
            dias_mora = (hoy - fecha_vencimiento).days

            if tasa_interes_mora > 0:
                 valor_intereses = valor_original * dias_mora * (tasa_interes_mora / 100)
            
            valor_total_calculado = valor_original + valor_intereses
        else:
            valor_total_calculado = valor_original
            
        valor_total_calculado = round(valor_total_calculado, 2)


        datos_deuda = data.dict()
        datos_deuda['valor_total'] = valor_total_calculado
        
        deuda = models.Deuda(**datos_deuda)
        db.add(deuda)
        db.commit()
        db.refresh(deuda)

        propietario = db.query(models.Propietario).filter(models.Propietario.id == deuda.propietario_id).first()

        if propietario and propietario.correo:
            asunto = "💰 Nueva deuda registrada"
            mensaje = mensaje_deuda(propietario, deuda)
            background_tasks.add_task(enviar_email, propietario.correo, asunto, mensaje)

        return deuda

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
