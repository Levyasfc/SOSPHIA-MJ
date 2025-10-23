from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship
from app.database import Base

class ComunicacionCobro(Base):
    __tablename__ = "comunicaciones_cobro"

    id = Column(Integer, primary_key=True, index=True)
    propietario_id = Column(Integer, ForeignKey("propietarios.id"), nullable=False)
    deuda_id = Column(Integer, ForeignKey("deudas.id"), nullable=False)

    medio = Column(String(50), nullable=False)  
    mensaje = Column(String(500), nullable=False)
    fecha_envio = Column(DateTime, default=datetime.utcnow)
    recibido = Column(Boolean, default=False) 
    autorizado_contacto = Column(Boolean, default=False)  

    propietario = relationship("Propietario", back_populates="comunicaciones")
    deuda = relationship("Deuda", back_populates="comunicaciones")