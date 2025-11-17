from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class HistorialJuridico(Base):
    __tablename__ = "historial_juridico"

    id = Column(Integer, primary_key=True, index=True)
    caso_id = Column(Integer, ForeignKey("casos_juridicos.id"), nullable=False)

    fecha = Column(DateTime, default=datetime.utcnow)
    descripcion = Column(Text, nullable=False)
    usuario = Column(String(150), nullable=True)

    caso = relationship("CasoJuridico", back_populates="historial")
