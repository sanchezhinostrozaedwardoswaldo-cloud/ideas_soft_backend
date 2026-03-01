from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.core.security import get_current_user
from app.models.cliente import Cliente
from app.models.usuario import Usuario
from app.schemas.carrito_schema import CarritoAgregar
from app.services.carrito_service import (
    agregar_al_carrito,
    obtener_mi_carrito,
    eliminar_item_carrito,
    convertir_carrito_en_venta
)

router = APIRouter(prefix="/carrito", tags=["Carrito"])

@router.post("/")
def agregar(
    data: CarritoAgregar,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    return agregar_al_carrito(db, current_user.id_cliente, data)


@router.get("/")
def listar(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    return obtener_mi_carrito(db, current_user.id_cliente)


@router.delete("/{id_detalle}")
def eliminar(
    id_detalle: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    eliminar_item_carrito(db, current_user.id_cliente, id_detalle)
    return {"mensaje": "Item eliminado"}


@router.post("/confirmar")
def confirmar_compra(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    return convertir_carrito_en_venta(db, current_user.id_cliente)

