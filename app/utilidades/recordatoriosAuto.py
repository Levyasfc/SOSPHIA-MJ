from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from app.common.plantillas.mensaje_deuda_vencida import mensaje_deuda_vencida
from sqlalchemy.orm import Session
from fastapi import BackgroundTasks
from app.database import get_db
from app import models, schemas
from app.utilidades.correos import enviar_email
from app.common.plantillas.Plantillabase import base_template

def revisar_deudas_vencidas(background_tasks: BackgroundTasks = None):
    db: Session = next(get_db())
    limite = datetime.utcnow() - timedelta(days=30)

    deudas = db.query(models.Deuda).filter(
        models.Deuda.fecha_limite < limite,
        models.Deuda.pagada == False
    ).all()

    for deuda_orm in deudas:
        propietario_orm = deuda_orm.propietario

        # 🔹 Convertimos los modelos ORM a schemas (DTOs)
        deuda = schemas.Deuda.from_orm(deuda_orm)
        propietario = schemas.Propietario.from_orm(propietario_orm)

        titulo = "Aviso de deuda vencida"
        contenido = mensaje_deuda_vencida(propietario, deuda)
        cuerpo = base_template(titulo, contenido)

        if background_tasks:
            background_tasks.add_task(enviar_email, propietario.correo, titulo, cuerpo)
        else:
            enviar_email(propietario.correo, titulo, cuerpo)

        if not getattr(deuda_orm, "caso_juridico", None):
            caso = models.CasoJuridico(
                deuda_id=deuda_orm.id,
                descripcion="Deuda vencida por más de 30 días",
                fecha_registro=datetime.utcnow()
            )
            db.add(caso)

    db.commit()
    db.close()


def iniciar_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(revisar_deudas_vencidas, 'cron', hour=6, minute=0)
    scheduler.start()
    print("🕕 Scheduler iniciado: revisión diaria de deudas a las 6:00 AM")

