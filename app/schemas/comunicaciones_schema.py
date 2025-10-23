from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ComunicacionCobroBase(BaseModel):
    canal: str  
    mensaje: str
    fecha_envio: Optional[datetime] = None

class ComunicacionCobroCreate(ComunicacionCobroBase):
    propietario_id: int

class ComunicacionCobro(ComunicacionCobroBase):
    id: int
    propietario_id: int

    class Config:
        from_attributes = True


class ComunicacionCobroUpdate(BaseModel):
    canal: Optional[str] = None
    mensaje: Optional[str] = None
    fecha_envio: Optional[datetime] = None
