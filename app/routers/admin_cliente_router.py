from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.core.security import require_role
from app.models.usuario import Usuario
from app.services.admin_cliente_service import (
    listar_clientes,
    cambiar_estado_cliente,
    detalle_cliente
)
from app.schemas.admin_cliente_schema import CambiarEstadoCliente
from fastapi.responses import StreamingResponse
from app.services.admin_cliente_service import exportar_clientes_excel


router = APIRouter(prefix="/admin/clientes", tags=["Admin Clientes"])


@router.get("/")
def listar(
    tipo: str | None = None,
    estado: str | None = None,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role("admin"))
):
    return listar_clientes(db, tipo, estado)


@router.patch("/{id_cliente}/estado")
def actualizar_estado(
    id_cliente: int,
    data: CambiarEstadoCliente,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role("admin"))
):

    cliente = cambiar_estado_cliente(db, id_cliente, data.estado)

    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    return {
        "message": "Estado actualizado correctamente",
        "id_cliente": cliente.id_cliente,
        "nuevo_estado": cliente.estado_cliente
    }


@router.get("/{id_cliente}")
def detalle(
    id_cliente: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role("admin"))
):

    data = detalle_cliente(db, id_cliente)

    if not data:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    return data

@router.get("/export/excel")
def exportar_excel(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role("admin"))
):

    file_stream = exportar_clientes_excel(db)

    return StreamingResponse(
        file_stream,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": "attachment; filename=clientes.xlsx"
        }
    )
