from __future__ import annotations
from sqlalchemy import Column, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Poder(Base):
    __tablename__ = "poderes"

    id = Column(Integer, primary_key=True, index=True)
    hp_id = Column(Integer, nullable=False)
    otorgante_id = Column(Integer, nullable=False)
    apoderado_id = Column(Integer, nullable=False)
    fecha_otorgado = Column(Date, nullable=False)
    fecha_expiracion = Column(Date, nullable=True)

