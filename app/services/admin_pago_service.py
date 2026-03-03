from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.pago import Pago
from datetime import datetime
from openpyxl import Workbook
from io import BytesIO

def obtener_pagos(
    db: Session,
    fecha_inicio: datetime | None = None,
    fecha_fin: datetime | None = None,
    metodo_pago: str | None = None,
    estado: str | None = None
):

    query = db.query(Pago)

    if fecha_inicio and fecha_fin:
        query = query.filter(
            Pago.fecha_pago.between(fecha_inicio, fecha_fin)
        )

    if metodo_pago:
        query = query.filter(Pago.metodo_pago == metodo_pago)

    if estado:
        query = query.filter(Pago.estado == estado)

    return query.order_by(Pago.fecha_pago.desc()).all()


def cambiar_estado_pago(db: Session, id_pago: int, nuevo_estado: str):

    pago = db.query(Pago).filter(
        Pago.id_pago == id_pago
    ).first()

    if not pago:
        return None

    pago.estado = nuevo_estado
    db.commit()
    db.refresh(pago)

    return pago


def exportar_pagos_excel(db: Session):

    pagos = db.query(Pago).all()

    wb = Workbook()
    ws = wb.active
    ws.title = "Pagos"

    ws.append([
        "ID Pago",
        "ID Cliente",
        "ID Venta",
        "Monto",
        "Fecha Pago",
        "Método",
        "Estado",
        "Referencia"
    ])

    for p in pagos:
        ws.append([
            p.id_pago,
            p.id_cliente,
            p.id_venta,
            float(p.monto),
            str(p.fecha_pago),
            p.metodo_pago,
            p.estado,
            p.referencia_pago
        ])

    file_stream = BytesIO()
    wb.save(file_stream)
    file_stream.seek(0)

    return file_stream
