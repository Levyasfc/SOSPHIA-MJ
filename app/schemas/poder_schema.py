from pydantic import BaseModel
from datetime import date
from typing import Optional

class PoderBase(BaseModel):
    otorgante_id: int
    apoderado_id: int
    fecha_otorgado: date
    fecha_expiracion: Optional[date] = None

class PoderCreate(PoderBase):
    pass

class Poder(PoderBase):
    id: int

    class Config:
        from_attributes = True
