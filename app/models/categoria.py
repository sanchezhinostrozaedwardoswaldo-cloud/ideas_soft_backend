from sqlalchemy import Column, Integer, String, Text
from app.database.base import Base

class Categoria(Base):
    __tablename__ = "categoria"

    id_categoria = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text)
    estado = Column(String(20), default="activo")
