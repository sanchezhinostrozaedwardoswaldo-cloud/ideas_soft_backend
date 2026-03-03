from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.schemas.categoria_schema import (
    CategoriaCreate,
    CategoriaUpdate,
    CategoriaResponse
)
from app.services.categoria_service import (
    get_all_categorias,
    create_categoria,
    update_categoria,
    desactivar_categoria
)
from app.core.security import require_role
from app.models.usuario import Usuario

router = APIRouter(prefix="/categorias", tags=["Categorias"])


# 🌐 Público
@router.get("/", response_model=list[CategoriaResponse])
def listar(db: Session = Depends(get_db)):
    return get_all_categorias(db)


# 🖥 Admin
@router.post("/", response_model=CategoriaResponse)
def crear(
    data: CategoriaCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role("admin"))
):
    return create_categoria(db, data)


@router.put("/{id_categoria}", response_model=CategoriaResponse)
def actualizar(
    id_categoria: int,
    data: CategoriaUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role("admin"))
):
    categoria = update_categoria(db, id_categoria, data)

    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria no encontrada")

    return categoria


@router.patch("/{id_categoria}/desactivar", response_model=CategoriaResponse)
def desactivar(
    id_categoria: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role("admin"))
):
    categoria = desactivar_categoria(db, id_categoria)

    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria no encontrada")

    return categoria
