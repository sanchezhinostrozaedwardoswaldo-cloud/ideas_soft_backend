from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, DECIMAL, CheckConstraint
from sqlalchemy.sql import func
from app.database.base import Base

class Pago(Base):
    __tablename__ = "pagos"

    id_pago = Column(Integer, primary_key=True, index=True)
    id_cliente = Column(Integer, ForeignKey("clientes.id_cliente"))
    id_venta = Column(Integer, ForeignKey("ventas.id_venta"), nullable=True)
    id_suscripcion = Column(Integer, ForeignKey("suscripciones.id_suscripcion"), nullable=True)
    
    monto = Column(DECIMAL(10, 2), nullable=False)
    fecha_pago = Column(DateTime, server_default=func.now())
    metodo_pago = Column(String(50))
    # Estados: 'completado', 'pendiente', 'cancelado'
    estado = Column(String(20))
    referencia_pago = Column(String(100))
    comprobante_url = Column(String(255))

    __table_args__ = (
        CheckConstraint(
            "estado IN ('completado', 'pendiente', 'cancelado')", 
            name="check_estado_pago"
        ),
    )