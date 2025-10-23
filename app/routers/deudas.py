from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.deuda import Deuda
from app.schemas.deuda_schema import DeudaCreate, DeudaResponse, DeudaCalculoResponse
from typing import List, Optional
from datetime import date
from decimal import Decimal, ROUND_HALF_UP

router = APIRouter(prefix="/deudas", tags=["Deudas"])

@router.post("/", response_model=DeudaResponse, status_code=status.HTTP_201_CREATED)
def crear_deuda(payload: DeudaCreate, db: Session = Depends(get_db)):
    nueva = Deuda(**payload.dict())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

@router.get("/", response_model=List[DeudaResponse])
def listar_deudas(propietario_id: Optional[int] = Query(None), db: Session = Depends(get_db)):
    q = db.query(Deuda)
    if propietario_id is not None:
        q = q.filter(Deuda.propietario_id == propietario_id)
    return q.all()

@router.get("/{deuda_id}", response_model=DeudaResponse)
def obtener_deuda(deuda_id: int, db: Session = Depends(get_db)):
    deuda = db.query(Deuda).filter(Deuda.id == deuda_id).first()
    if not deuda:
        raise HTTPException(status_code=404, detail="Deuda no encontrada")
    return deuda

def _calcular_interes(monto: Decimal, tasa_anual: Decimal, dias_mora: int) -> Decimal:
    tasa_diaria = (tasa_anual / Decimal(100)) / Decimal(365)
    interes = (monto * tasa_diaria * Decimal(dias_mora)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return interes

@router.get("/{deuda_id}/calcular", response_model=DeudaCalculoResponse)
def calcular_monto_deuda(deuda_id: int, on_date: Optional[date] = None, db: Session = Depends(get_db)):
    deuda = db.query(Deuda).filter(Deuda.id == deuda_id).first()
    if not deuda:
        raise HTTPException(status_code=404, detail="Deuda no encontrada")

    hoy = on_date or date.today()
    dias_mora = (hoy - deuda.fecha_vencimiento).days
    dias_mora = dias_mora if dias_mora > 0 else 0

    monto = Decimal(deuda.monto)
    tasa = Decimal(deuda.tasa_interes_anual or 0)

    interes = _calcular_interes(monto, tasa, dias_mora)
    total = (monto + interes).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    return DeudaCalculoResponse(
        id=deuda.id,
        monto_principal=monto,
        dias_mora=dias_mora,
        interes_acumulado=interes,
        monto_total_a_pagar=total
    )
