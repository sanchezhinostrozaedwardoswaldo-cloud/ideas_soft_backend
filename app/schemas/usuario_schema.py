from pydantic import BaseModel, EmailStr, Field
from enum import Enum


class UsuarioCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)


class UsuarioLogin(BaseModel):
    email: EmailStr
    password: str

class TipoCliente(str, Enum):
    empresa = "empresa"
    persona_natural = "persona_natural"

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)

    tipo_cliente: TipoCliente
    nombre_empresa: str | None = None
    ruc: str | None = None
    nombre_completo: str | None = None
    dni: str | None = None
    direccion: str
    telefono: str

