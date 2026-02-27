from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.base import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id_usuario = Column(Integer, primary_key=True, index=True)
    id_cliente = Column(Integer, ForeignKey("clientes.id_cliente", ondelete="CASCADE"))
    email = Column(String(150), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    rol = Column(String(20), nullable=False)
    estado = Column(String(20), default="activo")
    fecha_creacion = Column(TIMESTAMP, server_default=func.now())
    ultimo_login = Column(TIMESTAMP)
    token_recuperacion = Column(String(255))

    cliente = relationship("Cliente", back_populates="usuarios")
