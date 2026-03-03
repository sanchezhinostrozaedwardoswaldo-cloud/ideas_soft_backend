from sqlalchemy import Column, Integer, ForeignKey, Numeric, String, CheckConstraint
from app.database.base import Base
from sqlalchemy.orm import relationship

class DetalleVenta(Base):
    __tablename__ = "detalle_venta"

    id_detalle = Column(Integer, primary_key=True, index=True)
    id_venta = Column(Integer, ForeignKey("ventas.id_venta"))
    id_software = Column(Integer, ForeignKey("software.id_software"))
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Numeric, nullable=False)
    tipo_licencia = Column(String(20), nullable=False)

    venta = relationship("Venta", back_populates="detalles")
    software = relationship("Software")

    __table_args__ = (
        CheckConstraint(
            "tipo_licencia IN ('venta', 'suscripcion')", 
            name="check_tipo_licencia"
        ),
    )