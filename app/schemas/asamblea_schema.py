from __future__ import annotations
from datetime import datetime
from typing import Optional, List
from .votacion_schema import Votacion
from pydantic import BaseModel

class AsambleaBase(BaseModel):
    fecha: Optional[datetime] = None
    tipo: str
    descripcion: Optional[str] = None
    lugar: Optional[str] = None

class AsambleaCreate(AsambleaBase):
    pass

class Asamblea(AsambleaBase):
    id: int
    votaciones: Optional[List["Votacion"]] = None 

    model_config = {
        "from_attributes": True
    }

Asamblea.model_rebuild()
