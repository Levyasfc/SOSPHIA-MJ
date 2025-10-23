from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship
from app.database import Base

class PoderVotacion(Base):
    __tablename__ = "poderes_votaciones"

    id = Column(Integer, primary_key=True, index=True)
    propietario_id = Column(Integer, ForeignKey("propietarios.id"), nullable=False)

    tipo = Column(String(50), nullable=False) 
    descripcion = Column(String(300), nullable=True)  # detalle del poder o votación
    quorum_requerido = Column(Integer, nullable=True)  
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_votacion = Column(DateTime, nullable=True)
    resultado = Column(String(100), nullable=True)  # Ej: "Aprobado", "Rechazado", "Pendiente"
    acta_guardada = Column(Boolean, default=False)  

    propietario = relationship("Propietario", back_populates="poderes_votaciones")