from pydantic import BaseModel
from typing import Literal

class CambiarEstadoCliente(BaseModel):
    estado: Literal["activo", "bloqueado"]
