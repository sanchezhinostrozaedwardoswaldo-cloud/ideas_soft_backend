from sqlalchemy import Column, Integer, ForeignKey, Numeric
from app.database.base import Base

class DetalleVenta(Base):
    __tablename__ = "detalle_venta"

    id_detalle = Column(Integer, primary_key=True, index=True)
    id_venta = Column(Integer, ForeignKey("ventas.id_venta"))
    id_software = Column(Integer, ForeignKey("software.id_software"))
    cantidad = Column(Integer)
    precio_unitario = Column(Numeric)
