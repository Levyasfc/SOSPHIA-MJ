from sqlalchemy import Column, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Poder(Base):
    __tablename__ = "poderes"

    id = Column(Integer, primary_key=True, index=True)
    otorgante_id = Column(Integer, ForeignKey("propietarios.id", ondelete="CASCADE"), nullable=False)
    apoderado_id = Column(Integer, ForeignKey("propietarios.id", ondelete="CASCADE"), nullable=False)
    fecha_otorgado = Column(Date, nullable=False)
    fecha_expiracion = Column(Date, nullable=True)

    otorgante = relationship("Propietario", foreign_keys=[otorgante_id], back_populates="poderes_otorgados")
    apoderado = relationship("Propietario", foreign_keys=[apoderado_id], back_populates="poderes_recibidos")
