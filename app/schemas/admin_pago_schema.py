from pydantic import BaseModel
from typing import Literal

class CambiarEstadoPago(BaseModel):
    estado: Literal["completado", "pendiente", "cancelado"]
