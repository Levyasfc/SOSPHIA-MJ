from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app import schemas
from app.services.poder_service import PoderService

router = APIRouter(prefix="/poderes", tags=["Poderes"])

@router.post("/", response_model=schemas.Poder)
def crear_poder(data: schemas.PoderCreate, db: Session = Depends(get_db)):
    return PoderService.crear_poder(db, data)

@router.get("/", response_model=List[schemas.Poder])
def listar_poderes(db: Session = Depends(get_db)):
    return PoderService.obtener_poderes(db)

@router.delete("/{poder_id}")
def eliminar_poder(poder_id: int, db: Session = Depends(get_db)):
    return PoderService.eliminar_poder(db, poder_id)
