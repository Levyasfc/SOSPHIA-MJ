from __future__ import annotations
from sqlalchemy import Column, Integer, Float, String, DateTime, Boolean
from datetime import datetime
from sqlalchemy.orm import relationship
from app.database import Base


class Deuda(Base):
    __tablename__ = "deudas"

    id = Column(Integer, primary_key=True, index=True)
    hp_id = Column(Integer, nullable=False)
    propietario_id = Column(Integer, nullable=False)
    descripcion = Column(String(250))
    valor_original = Column(Float, nullable=False)
    interes_mora = Column(Float)
    valor_total = Column(Float, nullable=False)
    fecha_vencimiento = Column(DateTime, nullable=False)
    fecha_pago = Column(DateTime, nullable=True)
    pagado = Column(Boolean, default=False)

    comunicaciones = relationship("ComunicacionCobro", back_populates="deuda", cascade="all, delete-orphan")