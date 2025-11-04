from sqlalchemy import Column, Integer, DateTime, String, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Asamblea(Base):
    __tablename__ = "asambleas"

    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(DateTime, nullable=False, default=datetime.utcnow)
    tipo = Column(String(50), nullable=False)  # ej: "ordinaria", "extraordinaria"
    descripcion = Column(Text, nullable=True)
    lugar = Column(String(150), nullable=True)

    votaciones = relationship("Votacion", back_populates="asamblea", cascade="all, delete-orphan")
