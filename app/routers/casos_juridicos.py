from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app import schemas
from app.services.casos_juridicos_service import CasosJuridicosService

router = APIRouter(prefix="/{hp_id}/juridico", tags=["Jurídico"])

@router.post("/casos", response_model=schemas.CasoJuridico)
async def crear_caso(
    hp_id: int,
    data: schemas.CasoJuridicoCreate,
    user_id: int, 
    db: Session = Depends(get_db)
):
    return await CasosJuridicosService.crear_caso(db, data, hp_id, user_id)


@router.get("/casos", response_model=List[schemas.CasoJuridico])
def obtener_casos(
    hp_id: int,
    db: Session = Depends(get_db)
):
    return CasosJuridicosService.obtener_casos(db, hp_id)


@router.get("/casos/{caso_id}", response_model=schemas.CasoJuridico)
def obtener_caso(
    hp_id: int,
    caso_id: int,
    db: Session = Depends(get_db)
):
    return CasosJuridicosService.obtener_caso(db, caso_id, hp_id)


@router.post("/casos/{caso_id}/historial", response_model=schemas.HistorialJuridico)
async def agregar_historial(
    hp_id: int,
    caso_id: int,
    data: schemas.HistorialJuridicoCreate,
    user_id: int,
    db: Session = Depends(get_db)
):
    return await CasosJuridicosService.agregar_historial(db, caso_id, hp_id, data, user_id)

@router.patch("/casos/{caso_id}/estado", response_model=schemas.CasoJuridico)
def cambiar_estado(
    hp_id: int,
    caso_id: int,
    nuevo_estado: str,
    db: Session = Depends(get_db)
):
    return CasosJuridicosService.cambiar_estado(db, caso_id, hp_id, nuevo_estado)
