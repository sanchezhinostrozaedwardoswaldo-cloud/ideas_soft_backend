from sqlalchemy import Column, Integer, Text,DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.base import Base

class MensajeTicket(Base):
    __tablename__ = "mensajes_ticket"

    id_mensaje = Column(Integer, primary_key=True, index=True)
    id_ticket = Column(Integer, ForeignKey("soporte_tickets.id_ticket"))
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"))
    mensaje = Column(Text, nullable=False)
    fecha = Column(DateTime, server_default=func.now())

    ticket = relationship("SoporteTicket", back_populates="mensajes")
