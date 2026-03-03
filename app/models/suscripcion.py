from sqlalchemy import Column, Integer, String, Date, ForeignKey, CheckConstraint
from app.database.base import Base

class Suscripcion(Base):
    __tablename__ = "suscripciones"

    id_suscripcion = Column(Integer, primary_key=True, index=True)
    id_cliente = Column(Integer, ForeignKey("clientes.id_cliente"))
    id_software = Column(Integer, ForeignKey("software.id_software"))
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=False)
    # Estados: 'activo', 'vencido', 'cancelado'
    estado = Column(String(20), nullable=False)
    tipo_plan = Column(String(50), nullable=False)

    __table_args__ = (
        CheckConstraint(
            "estado IN ('activo', 'vencido', 'cancelado')", 
            name="check_estado_suscripcion"
        ),
    )