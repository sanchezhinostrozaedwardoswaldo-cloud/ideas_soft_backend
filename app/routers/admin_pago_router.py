from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app.database.connection import get_db
from app.core.security import require_role
from app.models.usuario import Usuario
from app.services.admin_pago_service import (
    obtener_pagos,
    cambiar_estado_pago
)
from app.schemas.admin_pago_schema import CambiarEstadoPago
from fastapi.responses import StreamingResponse
from app.services.admin_pago_service import exportar_pagos_excel


router = APIRouter(prefix="/admin/pagos", tags=["Admin Pagos"])


@router.get("/")
def listar_pagos(
    fecha_inicio: datetime | None = None,
    fecha_fin: datetime | None = None,
    metodo_pago: str | None = None,
    estado: str | None = None,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role("admin"))
):
    return obtener_pagos(
        db,
        fecha_inicio,
        fecha_fin,
        metodo_pago,
        estado
    )


@router.patch("/{id_pago}/estado")
def actualizar_estado(
    id_pago: int,
    data: CambiarEstadoPago,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role("admin"))
):

    pago = cambiar_estado_pago(db, id_pago, data.estado)

    if not pago:
        raise HTTPException(status_code=404, detail="Pago no encontrado")

    return {
        "message": "Estado actualizado correctamente",
        "id_pago": pago.id_pago,
        "nuevo_estado": pago.estado
    }

@router.get("/export/excel")
def exportar_excel(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role("admin"))
):

    file_stream = exportar_pagos_excel(db)

    return StreamingResponse(
        file_stream,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": "attachment; filename=pagos.xlsx"
        }
    )
