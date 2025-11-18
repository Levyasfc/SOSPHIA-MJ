from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from .historial_juridico_schema import HistorialJuridico


class CasoJuridicoCreate(BaseModel):
    motivo: str
    deuda_id: int
    notificar: bool = False
    correo_responsable: Optional[EmailStr] = None


class CasoJuridico(BaseModel):
    id: int
    hp_id: int
    deuda_id: int
    estado: str
    motivo: Optional[str]
    abogado: Optional[str]
    fecha_inicio: datetime
    fecha_cierre: Optional[datetime]

    historial: List[HistorialJuridico] = []

    class Config:
        from_attributes = True
