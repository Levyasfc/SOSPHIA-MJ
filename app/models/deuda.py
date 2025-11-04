from __future__ import annotations
from sqlalchemy import Column, Integer, Float, String, DateTime, Boolean, ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship
from app.database import Base


class Deuda(Base):
    __tablename__ = "deudas"

    id = Column(Integer, primary_key=True, index=True)
    propietario_id = Column(Integer, ForeignKey("propietarios.id"), nullable=False)
    descripcion = Column(String(250), nullable=True)
    valor_original = Column(Float, nullable=False)
    interes_mora = Column(Float, default=0.0)
    valor_total = Column(Float, nullable=False)
    fecha_vencimiento = Column(DateTime, nullable=False)
    fecha_pago = Column(DateTime, nullable=True)
    pagado = Column(Boolean, default=False)

    propietario = relationship("Propietario", back_populates="deudas")
    comunicaciones = relationship("ComunicacionCobro", back_populates="deuda", cascade="all, delete-orphan")