from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class PropietarioBase(BaseModel):
    nombre: str
    correo: EmailStr
    telefono: Optional[str] = None
    propiedadID: int
    autorizacion_datos: Optional[bool] = False
    fecha_autorizacion: Optional[datetime] = None

class PropietarioCreate(PropietarioBase):
    pass

class PropietarioResponse(PropietarioBase):
    id: int

    class Config:
        from_attributes = True  
