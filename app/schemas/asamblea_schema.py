from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class AsambleaBase(BaseModel):
    fecha: Optional[datetime] = None
    tipo: str
    descripcion: Optional[str] = None
    lugar: Optional[str] = None

class AsambleaCreate(AsambleaBase):
    pass

class Asamblea(AsambleaBase):
    id: int
    votaciones: Optional[List["Votacion"]] = []

    class Config:
        from_attributes = True
