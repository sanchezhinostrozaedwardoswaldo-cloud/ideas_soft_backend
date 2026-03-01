from sqlalchemy import Column, Integer, ForeignKey, String, Date
from app.database.base import Base

class Licencia(Base):
    __tablename__ = "licencias"

    id_licencia = Column(Integer, primary_key=True, index=True)
    id_suscripcion = Column(Integer, ForeignKey("suscripciones.id_suscripcion"), nullable=True)
    id_venta = Column(Integer, ForeignKey("ventas.id_venta"), nullable=True)

    clave_licencia = Column(String(255), nullable=False)

    fecha_activacion = Column(Date)
    fecha_expiracion = Column(Date)

    estado = Column(String(20))
    tipo_licencia = Column(String(20))
