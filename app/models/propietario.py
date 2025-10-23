from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from sqlalchemy.orm import relationship
from app.database import Base

class Propietario(Base):
    __tablename__ = "propietarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(150), nullable=False)
    correo = Column(String(150), nullable=False, index=True)
    telefono = Column(String(20), nullable=True) 
    propiedadID = Column(Integer, nullable=False)
    autorizacion_datos = Column(Boolean, default=False)
    fecha_autorizacion = Column(DateTime, nullable=True, default=datetime.utcnow)

    deudas = relationship("Deuda", back_populates="propietario", cascade="all, delete-orphan")
