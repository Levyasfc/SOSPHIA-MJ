from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List
from app.schemas.historial_juridico_schema import HistorialJuridico

class CasoJuridicoBase(BaseModel):
    titulo: str
    descripcion: str | None = None


class CasoJuridicoCreate(CasoJuridicoBase):
    pass


class CasoJuridico(CasoJuridicoBase):
    id: int
    hp_id: int
    estado: str
    fecha_creacion: datetime
    historial: list[HistorialJuridico] = []

    class Config:
        from_attributes = True

