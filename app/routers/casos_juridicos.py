from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app import schemas
from app.services.casos_juridicos_service import CasosJuridicosService

from app.common.Utilidades.usuarios import get_current_user
from app.common.Utilidades.permisos import validar_pertenencia_ph, validar_rol


router = APIRouter(prefix="/{hp_id}/casos-juridicos", tags=["Casos Jurídicos"])


@router.post("/", response_model=schemas.CasoJuridico)
async def crear_caso(
    hp_id: int,
    data: schemas.CasoJuridicoCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    usuario: dict = Depends(get_current_user)
):
    validar_pertenencia_ph(usuario, hp_id)
    validar_rol(usuario, ["ADMINISTRADOR", "ABOGADO"])

    return await CasosJuridicosService.crear_caso(
        db=db,
        data=data,
        hp_id=hp_id,
        user_id=usuario["user_id"],
        background_tasks=background_tasks
    )

@router.put("/{caso_id}/tomar", response_model=schemas.CasoJuridico)
async def tomar_caso(
    hp_id: int,
    caso_id: int,
    db: Session = Depends(get_db),
    usuario: dict = Depends(get_current_user)
):
    validar_pertenencia_ph(usuario, hp_id)
    validar_rol(usuario, ["ABOGADO", "ADMINISTRADOR"])

    return await CasosJuridicosService.tomar_caso(
        db=db,
        hp_id=hp_id,
        caso_id=caso_id,
        abogado_email=usuario["email"]
    )


@router.get("/", response_model=List[schemas.CasoJuridico])
def listar_casos(
    hp_id: int,
    db: Session = Depends(get_db),
    usuario: dict = Depends(get_current_user)
):
    validar_pertenencia_ph(usuario, hp_id)

    # Propietarios SOLO ven sus propios casos jurídicos
    if usuario["role"] == "PROPIETARIO TITULAR":
        return CasosJuridicosService.obtener_casos_por_usuario(
            db, hp_id, usuario["user_id"]
        )

    # Admin y abogados ven todos los casos
    validar_rol(usuario, ["ADMINISTRADOR", "ABOGADO"])
    return CasosJuridicosService.obtener_casos(db, hp_id)


@router.get("/{caso_id}", response_model=schemas.CasoJuridico)
def obtener_caso(
    hp_id: int,
    caso_id: int,
    db: Session = Depends(get_db),
    usuario: dict = Depends(get_current_user)
):
    validar_pertenencia_ph(usuario, hp_id)
    caso = CasosJuridicosService.obtener_caso(db, caso_id, hp_id)

    # Propietario: validar que la deuda sea de él
    if usuario["role"] == "PROPIETARIO TITULAR":
        if caso.deuda.propietario_id != usuario["user_id"]:
            raise HTTPException(status_code=403, detail="No puedes ver este caso jurídico")

    return caso


@router.post("/{caso_id}/historial", response_model=schemas.HistorialJuridico)
async def agregar_historial(
    hp_id: int,
    caso_id: int,
    data: schemas.HistorialJuridicoCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    usuario: dict = Depends(get_current_user)
):
    validar_pertenencia_ph(usuario, hp_id)
    validar_rol(usuario, ["ADMINISTRADOR", "ABOGADO"])

    return await CasosJuridicosService.agregar_historial(
        db=db,
        caso_id=caso_id,
        hp_id=hp_id,
        data=data,
        correo_usuario=usuario["email"],
        background_tasks=background_tasks
    )
