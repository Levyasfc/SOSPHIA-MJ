from __future__ import annotations
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ComunicacionCobroBase(BaseModel):
    propietario_id: int
    deuda_id: int
    medio: str
    mensaje: str
    recibido: bool = False
    autorizado_contacto: bool = False

# Para creación
class ComunicacionCobroCreate(ComunicacionCobroBase):
    pass

# Para actualización
class ComunicacionCobroUpdate(BaseModel):
    medio: Optional[str] = None
    mensaje: Optional[str] = None
    recibido: Optional[bool] = None
    autorizado_contacto: Optional[bool] = None

# Para respuesta
class ComunicacionCobro(ComunicacionCobroBase):
    id: int
    fecha_envio: datetime

    class Config:
        from_attributes = True

ComunicacionCobro.model_rebuild()