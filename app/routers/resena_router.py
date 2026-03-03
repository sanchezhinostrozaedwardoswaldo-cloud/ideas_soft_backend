from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.schemas.resena_schema import ResenaCreate, ResenaResponse
from app.services.resena_service import (
    crear_resena,
    obtener_resenas_por_software,
    cambiar_estado_resena
)
from app.core.security import get_current_user, require_role
from app.models.usuario import Usuario

router = APIRouter(prefix="/resenas", tags=["Reseñas"])


# 🌐 Cliente deja reseña
@router.post("/", response_model=ResenaResponse)
def crear(
    data: ResenaCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role("cliente"))
):
    return crear_resena(db, data, current_user.id_cliente)


# 🌐 Ver reseñas visibles de un software
@router.get("/software/{id_software}", response_model=list[ResenaResponse])
def listar_por_software(
    id_software: int,
    db: Session = Depends(get_db)
):
    return obtener_resenas_por_software(db, id_software)


# 🖥 Admin ocultar reseña
@router.patch("/{id_resena}/ocultar")
def ocultar(
    id_resena: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role("admin"))
):
    resena = cambiar_estado_resena(db, id_resena, "oculto")

    if not resena:
        raise HTTPException(status_code=404, detail="Reseña no encontrada")

    return {"mensaje": "Reseña ocultada correctamente"}


# 🖥 Admin mostrar reseña
@router.patch("/{id_resena}/mostrar")
def mostrar(
    id_resena: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role("admin"))
):
    resena = cambiar_estado_resena(db, id_resena, "visible")

    if not resena:
        raise HTTPException(status_code=404, detail="Reseña no encontrada")

    return {"mensaje": "Reseña visible nuevamente"}
