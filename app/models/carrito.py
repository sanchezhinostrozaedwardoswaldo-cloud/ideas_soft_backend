from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.base import Base

class Carrito(Base):
    __tablename__ = "carrito"

    id_carrito = Column(Integer, primary_key=True, index=True)
    id_cliente = Column(Integer, ForeignKey("clientes.id_cliente", ondelete="CASCADE"))
    estado = Column(String(20), default="activo")
    fecha_creacion = Column(TIMESTAMP, server_default=func.now())

    detalles = relationship("CarritoDetalle", back_populates="carrito", cascade="all, delete")
