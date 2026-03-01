from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.core.security import get_current_user
from app.models.usuario import Usuario
from app.services.ventas_service import completar_venta

router = APIRouter(prefix="/ventas", tags=["Ventas"])


@router.put("/{id_venta}/completar")
def completar(
    id_venta: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    return completar_venta(db, id_venta)
