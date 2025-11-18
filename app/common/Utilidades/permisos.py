from fastapi import HTTPException, status

def validar_rol(usuario, roles_permitidos: list[str]):
    if usuario["role"] not in roles_permitidos:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Este rol no tiene permisos"
        )


def validar_pertenencia_ph(usuario, hp_id: int):
    """
    Valida que el usuario pertenezca a la propiedad horizontal.
    Sin embargo, si el microservicio NO envía datos de residencia (resident = null),
    permitimos continuar para no bloquear el sistema.
    """


    if usuario["role"] in ["ADMINISTRADOR", "ADMINISTRADOR INMOBILIARIO"]:
        return


    residente = usuario.get("resident")
    if residente is None:
        return  
    
    unidad = residente.get("residential_unit")
    if not unidad:
        return  

    edificio = unidad.get("building")

    if edificio is None:
        return  

    if int(edificio) != int(hp_id):
        raise HTTPException(
            status_code=403,
            detail="El usuario no pertenece a esta propiedad horizontal"
        )
