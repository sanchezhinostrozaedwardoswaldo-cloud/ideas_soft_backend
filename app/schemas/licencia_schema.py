from pydantic import BaseModel
from typing import Optional
from datetime import date


class LicenciaDetalleResponse(BaseModel):
    id_licencia: int
    clave_licencia: str
    fecha_activacion: Optional[date] = None
    fecha_expiracion: Optional[date] = None
    estado: str
    tipo_licencia: str
    software: str

    class Config:
        from_attributes = True
