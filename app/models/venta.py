from sqlalchemy import Column, Integer, ForeignKey, Numeric, String, DateTime
from sqlalchemy.orm import relationship
from app.database.base import Base

class Venta(Base):
    __tablename__ = "ventas"

    id_venta = Column(Integer, primary_key=True, index=True)
    id_cliente = Column(Integer, ForeignKey("clientes.id_cliente"))
    total = Column(Numeric)
    estado = Column(String)
    fecha = Column(DateTime)

    cliente = relationship("Cliente")
