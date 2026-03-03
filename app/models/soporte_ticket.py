from sqlalchemy import Column, Integer, String, Text,DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.base import Base

class SoporteTicket(Base):
    __tablename__ = "soporte_tickets"

    id_ticket = Column(Integer, primary_key=True, index=True)
    id_cliente = Column(Integer, ForeignKey("clientes.id_cliente"))
    asunto = Column(String)
    mensaje = Column(Text)
    estado = Column(String, default="abierto")
    fecha_creacion = Column(DateTime, server_default=func.now())

    mensajes = relationship(
        "MensajeTicket",
        back_populates="ticket",
        cascade="all, delete"
    )
