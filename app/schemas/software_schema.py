from pydantic import BaseModel
from typing import Optional
from decimal import Decimal
from enum import Enum


class SoftwareBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    precio_venta: Optional[Decimal] = None
    precio_alquiler: Optional[Decimal] = None
    imagen_url: str


class SoftwareCreate(SoftwareBase):
    pass

class EstadoSoftware(str, Enum):
    activo = "activo"
    inactivo = "inactivo"

class SoftwareUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    precio_venta: Optional[Decimal] = None
    precio_alquiler: Optional[Decimal] = None
    imagen_url: Optional[str] = None
    estado: Optional[EstadoSoftware] = None


class SoftwareResponse(SoftwareBase):
    id_software: int
    estado: str

    class Config:
        from_attributes = True
