from fastapi import Header, HTTPException
from app.common.Utilidades.clientes import obtener_usuario_externo


async def get_current_user(hp_id: int, email: str = Header(None)):
    """
    Obtiene el usuario autenticado desde linea base (microservicio) usando HP_ID + email.
    """
    if email is None:
        raise HTTPException(401, "Falta el header 'email' en la petición")

    usuarios = await obtener_usuario_externo(hp_id)

    usuario = None
    if isinstance(usuarios, list):
        for u in usuarios:
            if u.get("email") == email:
                usuario = u
                break

    if not usuario:
        raise HTTPException(404, f"El usuario con email {email} no pertenece a esta PH")

    return usuario
