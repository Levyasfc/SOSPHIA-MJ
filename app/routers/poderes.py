from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app import schemas
from app.services.poder_service import PoderService

router = APIRouter(prefix="/{hp_id}/poderes", tags=["Poderes"])

@router.post("/", response_model=schemas.Poder)
async def crear_poder(
    hp_id: int,
    data: schemas.PoderCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    return await PoderService.crear_poder(db, data, hp_id, background_tasks)


@router.get("/", response_model=List[schemas.Poder])
def listar_poderes(hp_id: int, db: Session = Depends(get_db)):
    return PoderService.obtener_poderes(db, hp_id)


@router.delete("/{poder_id}")
def eliminar_poder(poder_id: int, hp_id: int, db: Session = Depends(get_db)):
    return PoderService.eliminar_poder(db, poder_id, hp_id)