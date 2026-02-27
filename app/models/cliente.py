from sqlalchemy import Column, Integer, String, TIMESTAMP, CheckConstraint, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.base import Base

class Cliente(Base):
    __tablename__ = "clientes"

    id_cliente = Column(Integer, primary_key=True, index=True)
    tipo_cliente = Column(String(20), nullable=False)
    nombre_empresa = Column(String(150))
    ruc = Column(String(20))
    nombre_completo = Column(String(150))
    dni = Column(String(20))
    direccion = Column(String(200))
    telefono = Column(String(20))
    email = Column(String(150), unique=True, nullable=False)
    estado_cliente = Column(String(20), default="activo")
    fecha_registro = Column(TIMESTAMP, server_default=func.now())

    usuarios = relationship("Usuario", back_populates="cliente", cascade="all, delete")
