from __future__ import annotations
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class VotacionBase(BaseModel):
    asamblea_id: int
    propuesta: str

class VotacionCreate(VotacionBase):
    pass

class Votacion(VotacionBase):
    id: int
    votos_favor: int = 0
    votos_contra: int = 0
    abstenciones: int = 0
    resultado: Optional[str] = None

    class Config:
        from_attributes = True

Votacion.model_rebuild()