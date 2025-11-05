# app/routers/asambleas.py
from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app import schemas
from app.services.asamblea_service import AsambleaService

router = APIRouter(prefix="/asambleas", tags=["Asambleas"])

# Observa: background_tasks IS NOT Depends()
@router.post("/", response_model=schemas.Asamblea)
def crear_asamblea(
    data: schemas.AsambleaCreate,
    db: Session = Depends(get_db),
    background_tasks: BackgroundTasks = BackgroundTasks() 
):
    
    return AsambleaService.crear_asamblea(db, data, background_tasks)

@router.get("/", response_model=List[schemas.Asamblea])
def listar_asambleas(db: Session = Depends(get_db)):
    return AsambleaService.obtener_asambleas(db)

@router.get("/{asamblea_id}", response_model=schemas.Asamblea)
def obtener_asamblea(asamblea_id: int, db: Session = Depends(get_db)):
    return AsambleaService.obtener_asamblea(db, asamblea_id)
