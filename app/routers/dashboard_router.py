from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.core.security import require_role
from app.models.usuario import Usuario
from app.services.dashboard_service import (
    resumen_general,
    software_mas_vendido,
    clientes_con_mas_compras
)
from fastapi.responses import StreamingResponse
from app.services.dashboard_service import generar_reporte_pdf

router = APIRouter(prefix="/admin/dashboard", tags=["Admin Dashboard"])


@router.get("/resumen")
def resumen(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role("admin"))
):
    return resumen_general(db)


@router.get("/software-top")
def top_software(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role("admin"))
):
    return software_mas_vendido(db)


@router.get("/clientes-top")
def top_clientes(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role("admin"))
):
    return clientes_con_mas_compras(db)

@router.get("/reporte/pdf")
def reporte_pdf(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role("admin"))
):

    pdf_buffer = generar_reporte_pdf(db)

    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": "attachment; filename=reporte_general.pdf"
        }
    )
