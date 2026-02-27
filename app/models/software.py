from sqlalchemy import Column, Integer, String, Text, DECIMAL
from app.database.base import Base


class Software(Base):
    __tablename__ = "software"

    id_software = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(150), nullable=False)
    descripcion = Column(Text)
    precio_venta = Column(DECIMAL(10, 2))
    precio_alquiler = Column(DECIMAL(10, 2))
    imagen_url = Column(String(255), nullable=False)
    estado = Column(String(20), default="activo")
