from sqlalchemy import Column, Integer, ForeignKey, String, Numeric, Date, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Deuda(Base):
    __tablename__ = "deudas"

    id = Column(Integer, primary_key=True, index=True)
    propietario_id = Column(Integer, ForeignKey("propietarios.id"), nullable=False)
    concepto = Column(String(200), nullable=False)
    monto = Column(Numeric(12,2), nullable=False)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_vencimiento = Column(Date, nullable=False)
    tasa_interes_anual = Column(Numeric(5,2), default=0.00)
    estado = Column(String(30), default="pendiente")
    observaciones = Column(String(400), nullable=True)

    propietario = relationship("Propietario", back_populates="deudas")
