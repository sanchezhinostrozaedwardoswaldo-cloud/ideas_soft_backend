from pydantic import BaseModel, Field
from datetime import datetime


class ResenaCreate(BaseModel):
    id_software: int
    comentario: str
    calificacion: int = Field(ge=1, le=5)


class ResenaResponse(BaseModel):
    id_resena: int
    id_cliente: int
    id_software: int
    comentario: str
    calificacion: int
    fecha: datetime
    estado: str

    class Config:
        from_attributes = True
