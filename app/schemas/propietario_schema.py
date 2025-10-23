from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class PropietarioBase(BaseModel):
    nombre: str
    correo: EmailStr
    telefono: Optional[str] = None
    propiedadID: int
    autorizacion_datos: Optional[bool] = False

class PropietarioCreate(PropietarioBase):
    pass

class PropietarioUpdate(BaseModel):
    nombre: Optional[str] = None
    correo: Optional[EmailStr] = None
    telefono: Optional[str] = None
    autorizacion_datos: Optional[bool] = None

class Propietario(PropietarioBase):
    id: int
    fecha_autorizacion: Optional[datetime] = None

    class Config:
        from_attributes = True
