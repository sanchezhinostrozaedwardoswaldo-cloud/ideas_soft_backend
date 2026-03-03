from sqlalchemy import Column, Integer, String, Text
from app.database.base import Base


class ConfiguracionSistema(Base):
    __tablename__ = "configuracion_sistema"

    id_config = Column(Integer, primary_key=True, index=True)
    clave = Column(String, unique=True, nullable=False)
    valor = Column(Text, nullable=False)
