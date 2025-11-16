from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from app.database import get_db
from app import schemas
from app.services.asamblea_service import AsambleaService

router = APIRouter(prefix="/{hp_id}/asambleas", tags=["Asambleas"])

@router.post("/", response_model=schemas.Asamblea)
async def crear_asamblea(
    hp_id: int,
    data: schemas.AsambleaCreate,
    db: Session = Depends(get_db),
    background_tasks: BackgroundTasks = BackgroundTasks(),
):
    return await AsambleaService.crear_asamblea(db, data, hp_id, background_tasks)


@router.get("/", response_model=list[schemas.Asamblea])
def listar_asambleas(hp_id: int, db: Session = Depends(get_db)):
    return AsambleaService.obtener_asambleas(db, hp_id)


@router.get("/{asamblea_id}", response_model=schemas.Asamblea)
def obtener_asamblea(hp_id: int, asamblea_id: int, db: Session = Depends(get_db)):
    return AsambleaService.obtener_asamblea(db, asamblea_id, hp_id)
