from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Base con campos comunes
class DeudaBase(BaseModel):
    propietario_id: int
    descripcion: Optional[str] = None
    valor_original: float
    interes_mora: Optional[float] = 0.0
    valor_total: float
    fecha_vencimiento: datetime
    pagado: Optional[bool] = False
    fecha_pago: Optional[datetime] = None

# Para creación
class DeudaCreate(DeudaBase):
    pass

# Para actualización
class DeudaUpdate(BaseModel):
    descripcion: Optional[str] = None
    valor_original: Optional[float] = None
    interes_mora: Optional[float] = None
    valor_total: Optional[float] = None
    fecha_vencimiento: Optional[datetime] = None
    pagado: Optional[bool] = None
    fecha_pago: Optional[datetime] = None

# Para respuesta
class Deuda(DeudaBase):
    id: int

    class Config:
        orm_mode = True
