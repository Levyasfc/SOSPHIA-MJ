from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from app.database import Base

class BienComun(Base):
    __tablename__ = "bienes_comunes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(150), nullable=False)  
    descripcion = Column(String(300), nullable=True)
    responsable = Column(String(150), nullable=True)  
    estado = Column(String(50), default="Activo")  # Ej: "Activo", "En mantenimiento", "Inactivo"
    requiere_autorizacion = Column(Boolean, default=False) 
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_actualizacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)