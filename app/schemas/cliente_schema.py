from pydantic import BaseModel, EmailStr
from typing import Optional

class ClienteCreate(BaseModel):
    tipo_cliente: str
    nombre_empresa: Optional[str] = None
    ruc: Optional[str] = None
    nombre_completo: Optional[str] = None
    dni: Optional[str] = None
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    email: EmailStr
