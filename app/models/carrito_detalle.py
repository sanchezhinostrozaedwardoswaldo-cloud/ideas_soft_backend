from sqlalchemy import Column, Integer, ForeignKey, DECIMAL, String
from sqlalchemy.orm import relationship
from app.database.base import Base

class CarritoDetalle(Base):
    __tablename__ = "carrito_detalle"

    id_detalle = Column(Integer, primary_key=True, index=True)
    id_carrito = Column(Integer, ForeignKey("carrito.id_carrito", ondelete="CASCADE"))
    id_software = Column(Integer, ForeignKey("software.id_software"))
    cantidad = Column(Integer, nullable=False)
    precio = Column(DECIMAL(10,2), nullable=False)
    tipo_operacion = Column(String(20), nullable=False)

    carrito = relationship("Carrito", back_populates="detalles")
