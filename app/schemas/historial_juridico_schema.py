from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List

class HistorialJuridicoBase(BaseModel):
    descripcion: str


class HistorialJuridicoCreate(HistorialJuridicoBase):
    pass


class HistorialJuridico(HistorialJuridicoBase):
    id: int
    caso_id: int
    usuario: str
    fecha: datetime

    class Config:
        orm_mode = True

