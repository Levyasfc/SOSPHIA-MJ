from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class CasoJuridico(Base):
    __tablename__ = "casos_juridicos"

    id = Column(Integer, primary_key=True, index=True)

    hp_id = Column(Integer, nullable=False)
    deuda_id = Column(Integer, ForeignKey("deudas.id"), nullable=False)

    estado = Column(String(50), default="En revisión")
    motivo = Column(Text, nullable=True)
    abogado = Column(String(150), nullable=True)

    fecha_inicio = Column(DateTime, default=datetime.utcnow)
    fecha_cierre = Column(DateTime, nullable=True)

    historial = relationship("HistorialJuridico", back_populates="caso",
                             cascade="all, delete-orphan")
