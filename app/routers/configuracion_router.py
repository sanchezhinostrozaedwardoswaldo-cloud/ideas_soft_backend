from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.core.security import require_role
from app.models.usuario import Usuario
from app.services.configuracion_service import (
    obtener_configuracion,
    actualizar_configuracion
)

router = APIRouter(
    prefix="/admin/configuracion",
    tags=["Configuración Sistema"]
)


@router.get("/")
def listar_configuracion(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role(["admin"]))
):
    return obtener_configuracion(db)


@router.put("/{clave}")
def actualizar(
    clave: str,
    nuevo_valor: str,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role(["admin"]))
):
    return actualizar_configuracion(db, clave, nuevo_valor)
