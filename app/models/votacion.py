from __future__ import annotations
from sqlalchemy import Column, Integer, ForeignKey, String, Text
from sqlalchemy.orm import relationship
from app.database import Base

class Votacion(Base):
    __tablename__ = "votaciones"

    id = Column(Integer, primary_key=True, index=True)
    asamblea_id = Column(Integer, ForeignKey("asambleas.id", ondelete="CASCADE"), nullable=False)
    propuesta = Column(Text, nullable=False)
    votos_favor = Column(Integer, default=0)
    votos_contra = Column(Integer, default=0)
    abstenciones = Column(Integer, default=0)
    resultado = Column(String(50), nullable=True)  # "Aprobado", "Rechazado", "Pendiente"

    asamblea = relationship("Asamblea", back_populates="votaciones")
