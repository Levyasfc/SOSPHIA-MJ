from sqlalchemy.orm import Session
from fastapi import BackgroundTasks, HTTPException
from app import models, schemas
from datetime import datetime, timezone
from app.utilidades.correos import enviar_email
from app.common.plantillas.deudas import mensaje_deuda
from app.common.Utilidades.clientes import obtener_usuario_externo

class DeudasService:

    @staticmethod
    async def crear_deuda(db: Session, data: schemas.DeudaCreateSinHP, background_tasks: BackgroundTasks, hp_id: int):

        # === VALIDAR QUE EL PROPIETARIO PERTENECE A LA PH ===
        usuarios = await obtener_usuario_externo(hp_id)

        # uniformar
        if isinstance(usuarios, dict):
            usuarios = [usuarios]

        propietario = next(
            (u for u in usuarios if u.get("user_id") == data.propietario_id),
            None
        )

        if not propietario:
            raise HTTPException(
                status_code=400,
                detail="El propietario NO pertenece a esta propiedad horizontal"
            )

        # === CALCULO DE INTERESES ===
        hoy = datetime.now(timezone.utc).date()
        fecha_vencimiento = data.fecha_vencimiento.date()

        valor_original = data.valor_original
        tasa_interes_mora = data.interes_mora
        valor_intereses = 0.0

        if hoy > fecha_vencimiento and tasa_interes_mora > 0:
            dias_mora = (hoy - fecha_vencimiento).days
            valor_intereses = valor_original * (dias_mora / 30) * (tasa_interes_mora / 100)

        valor_total_calculado = round(valor_original + valor_intereses, 2)

        # === CREAR DEUDA ===
        datos_deuda = data.dict()
        datos_deuda["valor_total"] = valor_total_calculado
        datos_deuda["hp_id"] = hp_id

        deuda = models.Deuda(**datos_deuda)
        db.add(deuda)
        db.commit()
        db.refresh(deuda)

        correo = propietario.get("email")
        person = propietario.get("person") or {}
        nombre = person.get("first_name", "Propietario")
        apellido = person.get("last_name", "")

        if correo:
            asunto = "💰 Nueva deuda registrada"
            mensaje = mensaje_deuda(
                {"nombre": nombre, "apellido": apellido},
                deuda
            )
            background_tasks.add_task(enviar_email, correo, asunto, mensaje)

        return deuda


    @staticmethod
    def obtener_deudas(db: Session, hp_id: int):
        return db.query(models.Deuda).filter_by(hp_id=hp_id).all()

    @staticmethod
    def obtener_deuda(db: Session, deuda_id: int, hp_id: int):
        deuda = db.query(models.Deuda).filter_by(id=deuda_id, hp_id=hp_id).first()
        if not deuda:
            raise HTTPException(status_code=404, detail="Deuda no encontrada")
        return deuda

    @staticmethod
    def actualizar_deuda(db: Session, deuda_id: int, data: schemas.DeudaUpdate, hp_id: int):
        deuda = db.query(models.Deuda).filter_by(id=deuda_id, hp_id=hp_id).first()
        if not deuda:
            raise HTTPException(status_code=404, detail="Deuda no encontrada")

        if deuda.pagado:
            raise HTTPException(status_code=400, detail="La deuda ya está pagada y no puede ser editada")

        deuda.descripcion = data.descripcion or deuda.descripcion
        deuda.interes_mora = data.interes_mora if data.interes_mora is not None else deuda.interes_mora
        deuda.valor_original = data.valor_original or deuda.valor_original

        deuda.valor_total = deuda.valor_original + deuda.interes_mora

        if data.pagado is True and not deuda.pagado:
            deuda.pagado = True
            deuda.fecha_pago = datetime.utcnow()

        db.commit()
        db.refresh(deuda)
        return deuda

    @staticmethod
    def eliminar_deuda(db: Session, deuda_id: int, hp_id: int):
        deuda = db.query(models.Deuda).filter_by(id=deuda_id, hp_id=hp_id).first()
        if not deuda:
            raise HTTPException(status_code=404, detail="Deuda no encontrada")

        db.delete(deuda)
        db.commit()
        return {"message": "Deuda eliminada exitosamente"}
