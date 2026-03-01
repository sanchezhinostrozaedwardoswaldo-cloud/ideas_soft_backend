from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.core.security import get_current_user
from app.models.venta import Venta
from app.models.licencia import Licencia
from app.models.detalle_venta import DetalleVenta
from app.models.software import Software
from app.models.usuario import Usuario
from app.schemas.licencia_schema import LicenciaDetalleResponse

router = APIRouter(prefix="/cliente", tags=["Panel Cliente"])

@router.get("/mis-ventas")
def mis_ventas(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    ventas = db.query(Venta).filter(
        Venta.id_cliente == current_user.id_cliente
    ).all()

    return ventas

@router.get("/mis-licencias")
def mis_licencias(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    licencias = db.query(Licencia)\
        .join(Venta, Licencia.id_venta == Venta.id_venta)\
        .filter(
            Venta.id_cliente == current_user.id_cliente,
            Licencia.estado == "activa"
        ).all()

    return licencias


@router.get(
    "/mis-licencias-detalle",
    response_model=list[LicenciaDetalleResponse]
)
def mis_licencias_detalle(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    resultados = db.query(
        Licencia,
        Software.nombre
    ).join(
        Venta, Licencia.id_venta == Venta.id_venta
    ).join(
        DetalleVenta, Venta.id_venta == DetalleVenta.id_venta
    ).join(
        Software, DetalleVenta.id_software == Software.id_software
    ).filter(
        Venta.id_cliente == current_user.id_cliente
    ).all()

    return [
    LicenciaDetalleResponse(
        id_licencia=licencia.id_licencia,
        clave_licencia=licencia.clave_licencia,
        fecha_activacion=licencia.fecha_activacion,
        fecha_expiracion=licencia.fecha_expiracion,
        estado=licencia.estado,
        tipo_licencia=licencia.tipo_licencia,
        software=nombre_software
    )
    for licencia, nombre_software in resultados
    ]

