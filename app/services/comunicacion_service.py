from datetime import datetime, time
from fastapi import HTTPException
from app.utilidades.notificaciones import enviar_correo, enviar_whatsapp

class ComunicacionService:

    @staticmethod
    def validar_horario():
        hora_actual = datetime.now().time()
        inicio = time(8, 0)
        fin = time(20, 0)

        if not (inicio <= hora_actual <= fin):
            raise HTTPException(status_code=400, detail="La comunicación solo puede enviarse entre 8am y 8pm (Ley 2300).")

    @staticmethod
    def validar_autorizacion_contacto(propietario):
        if not propietario.autoriza_contacto:
            raise HTTPException(status_code=400, detail="El propietario no ha autorizado contacto.")

    @staticmethod
    def enviar_notificacion(medio, propietario, mensaje):
        if medio == "email":
            enviar_correo(propietario.email, mensaje)
        elif medio == "whatsapp":
            enviar_whatsapp(propietario.telefono, mensaje)
        else:
            pass  # Registrar sin enviar
