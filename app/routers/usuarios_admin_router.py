from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.core.security import require_role
from app.models.usuario import Usuario
from app.services.usuarios_admin_service import (
    listar_usuarios_internos,
    crear_usuario_interno,
    cambiar_estado_usuario,
    cambiar_password_usuario
)

router = APIRouter(
    prefix="/admin/usuarios",
    tags=["Gestión Administradores"]
)


@router.get("/")
def listar(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role(["admin"]))
):
    return listar_usuarios_internos(db)


@router.post("/")
def crear(
    email: str,
    password: str,
    rol: str,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role(["admin"]))
):
    return crear_usuario_interno(db, email, password, rol)


@router.patch("/{id_usuario}/estado")
def cambiar_estado(
    id_usuario: int,
    nuevo_estado: str,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role(["admin"]))
):
    return cambiar_estado_usuario(db, id_usuario, nuevo_estado)


@router.patch("/{id_usuario}/password")
def cambiar_password(
    id_usuario: int,
    nueva_password: str,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role(["admin"]))
):
    return cambiar_password_usuario(db, id_usuario, nueva_password)
