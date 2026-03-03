from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.core.security import require_role
from app.models.usuario import Usuario
from app.services.panel_service import (
    obtener_compras_cliente,
    obtener_suscripciones_cliente,
    obtener_licencias_cliente,
    obtener_pagos_cliente
)

router = APIRouter(prefix="/panel", tags=["Panel Cliente"])


@router.get("/compras")
def compras(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role("cliente"))
):
    return obtener_compras_cliente(db, current_user.id_cliente)


@router.get("/suscripciones")
def suscripciones(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role("cliente"))
):
    return obtener_suscripciones_cliente(db, current_user.id_cliente)


@router.get("/licencias")
def licencias(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role("cliente"))
):
    return obtener_licencias_cliente(db, current_user.id_cliente)


@router.get("/pagos")
def pagos(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role("cliente"))
):
    return obtener_pagos_cliente(db, current_user.id_cliente)
