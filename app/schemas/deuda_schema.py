from pydantic import BaseModel, condecimal
from datetime import date, datetime
from typing import Optional

Decimal = condecimal(max_digits=12, decimal_places=2)

class DeudaBase(BaseModel):
    propietario_id: int
    concepto: str
    monto: int
    fecha_vencimiento: date
    tasa_interes_anual: Optional[float] = 0.00
    observaciones: Optional[str] = None

class DeudaCreate(DeudaBase):
    pass

class DeudaResponse(DeudaBase):
    id: int
    fecha_creacion: datetime
    estado: str

    class Config:
        from_attributes = True  

class DeudaCalculoResponse(BaseModel):
    id: int
    monto_principal: float
    dias_mora: int
    interes_acumulado: float
    monto_total_a_pagar: float