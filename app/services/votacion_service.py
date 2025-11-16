from sqlalchemy.orm import Session
from fastapi import HTTPException, BackgroundTasks
from app import models, schemas
from app.utilidades.correos import enviar_email
from app.common.plantillas.votacion import mensaje_confirmacion_voto
from app.common.Utilidades.clientes import obtener_usuario_externo


class VotacionService:

    @staticmethod
    def crear_votacion(db: Session, data: schemas.VotacionCreate, hp_id: int):
        asamblea = db.query(models.Asamblea).filter_by(id=data.asamblea_id, hp_id=hp_id).first()
        if not asamblea:
            raise HTTPException(status_code=404, detail="Asamblea no encontrada en esta PH")

        vot = models.Votacion(
            hp_id=hp_id,
            asamblea_id=data.asamblea_id,
            propuesta=data.propuesta
        )
        db.add(vot)
        db.commit()
        db.refresh(vot)
        return vot

    @staticmethod
    async def votar(db: Session, votacion_id: int, hp_id: int, usuario_id: int,
                    favor: int, contra: int, abstencion: int, background_tasks: BackgroundTasks):
        

    
        # 1️⃣ Buscar votación
        v = db.query(models.Votacion).filter_by(id=votacion_id, hp_id=hp_id).first()
        if not v:
            raise HTTPException(status_code=404, detail="Votación no encontrada en esta propiedad horizontal")

        # 2️⃣ Validar que solo envió un voto y que sea 1
        total = favor + contra + abstencion

        if total == 0:
            raise HTTPException(status_code=400, detail="Debe enviar 1 voto: favor, contra o abstención")

        if total > 1:
            raise HTTPException(status_code=400, detail="Solo puede votar en una opción")

        if favor not in (0, 1) or contra not in (0, 1) or abstencion not in (0, 1):
            raise HTTPException(status_code=400, detail="Los votos solo pueden ser 0 o 1")

        # 3️⃣ Verificar si el usuario ya votó
        voto_existente = db.query(models.Voto).filter_by(
            votacion_id=votacion_id,
            hp_id=hp_id,
            usuario_id=usuario_id
        ).first()

        if voto_existente:
            raise HTTPException(status_code=400, detail="Este usuario ya votó en esta votación")

        # 4️⃣ Registrar el voto
        if favor == 1:
            voto_texto = "favor"
            v.votos_favor += 1
        elif contra == 1:
            voto_texto = "contra"
            v.votos_contra += 1
        else:
            voto_texto = "abstencion"
            v.abstenciones += 1

        nuevo_voto = models.Voto(
            hp_id=hp_id,
            votacion_id=votacion_id,
            usuario_id=usuario_id,
            voto=voto_texto
        )
        db.add(nuevo_voto)

        # 5️⃣ Recalcular resultado
        if v.votos_favor > v.votos_contra:
            v.resultado = "Aprobado"
        elif v.votos_contra > v.votos_favor:
            v.resultado = "Rechazado"
        else:
            v.resultado = "Empate"

        db.commit()
        db.refresh(v)

        # 6️⃣ Enviar correo — SIN CAMBIOS
        usuarios = await obtener_usuario_externo(hp_id)
        correo = None
        nombre = ""


        if isinstance(usuarios, list):
            for u in usuarios:
                if u.get("user_id") == usuario_id:
                    correo = u.get("email")
                    nombre = u.get("person", {}).get("first_name", "Usuario")
                    break

        if correo:
            asunto = "🗳 Confirmación de voto"
            mensaje = mensaje_confirmacion_voto(nombre, v.propuesta)
            background_tasks.add_task(enviar_email, correo, asunto, mensaje)

        return v

    @staticmethod
    def obtener_votaciones(db: Session, hp_id: int):
        return db.query(models.Votacion).filter_by(hp_id=hp_id).all()
