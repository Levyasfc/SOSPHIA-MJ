from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class HistorialJuridicoCreate(BaseModel):
    descripcion: str
    notificar: bool = False
    correo_responsable: Optional[EmailStr] = None


class HistorialJuridico(BaseModel):
    id: int
    caso_id: int
    descripcion: str
    usuario: str
    fecha: datetime

    class Config:
        from_attributes = True