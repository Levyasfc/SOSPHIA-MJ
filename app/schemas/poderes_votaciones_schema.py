from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class PoderVotacionBase(BaseModel):
    tipo: str
    descripcion: Optional[str] = None
    quorum_requerido: Optional[int] = None
    fecha_votacion: Optional[datetime] = None
    resultado: Optional[str] = None
    acta_guardada: Optional[bool] = False

class PoderVotacionCreate(PoderVotacionBase):
    propietario_id: int

class PoderVotacion(PoderVotacionBase):
    id: int
    propietario_id: int

    class Config:
        from_attributes = True