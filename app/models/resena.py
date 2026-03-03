from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, CheckConstraint
from sqlalchemy.sql import func
from app.database.base import Base

class Resena(Base):
    __tablename__ = "resenas"

    id_resena = Column(Integer, primary_key=True, index=True)
    id_cliente = Column(Integer, ForeignKey("clientes.id_cliente"), nullable=True)
    id_software = Column(Integer, ForeignKey("software.id_software"), nullable=True)
    comentario = Column(Text)
    calificacion = Column(Integer)
    fecha = Column(DateTime, server_default=func.now())
    estado = Column(String(20), default="visible")

    # Restricción de base de datos para la calificación
    __table_args__ = (
        CheckConstraint('calificacion >= 1 AND calificacion <= 5', name='check_calificacion_rango'),
    )