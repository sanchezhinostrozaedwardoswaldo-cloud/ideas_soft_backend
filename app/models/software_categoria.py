from sqlalchemy import Column, Integer, ForeignKey
from app.database.base import Base

class SoftwareCategoria(Base):
    __tablename__ = "software_categoria"

    id_software = Column(Integer, ForeignKey("software.id_software"), primary_key=True)
    id_categoria = Column(Integer, ForeignKey("categoria.id_categoria"), primary_key=True)