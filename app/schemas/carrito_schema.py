from pydantic import BaseModel
from typing import Literal

class CarritoAgregar(BaseModel):
    id_software: int
    cantidad: int
    tipo_operacion: Literal["venta", "suscripcion"]
