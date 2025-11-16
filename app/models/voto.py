from sqlalchemy import Column, Integer, ForeignKey, String
from app.database import Base

class Voto(Base):
    __tablename__ = "votos"

    id = Column(Integer, primary_key=True, index=True)
    hp_id = Column(Integer, nullable=False)
    votacion_id = Column(Integer, ForeignKey("votaciones.id", ondelete="CASCADE"), nullable=False)
    usuario_id = Column(Integer, nullable=False) 
    voto = Column(String(20), nullable=False)  
