from sqlalchemy.orm import Session
from app.models.cliente import Cliente
from app.models.venta import Venta
from app.models.suscripcion import Suscripcion
from app.models.pago import Pago
from app.models.licencia import Licencia
from openpyxl import Workbook
from fastapi.responses import StreamingResponse
from io import BytesIO


def listar_clientes(db: Session, tipo: str | None = None, estado: str | None = None):

    query = db.query(Cliente)

    if tipo:
        query = query.filter(Cliente.tipo_cliente == tipo)

    if estado:
        query = query.filter(Cliente.estado_cliente == estado)

    return query.order_by(Cliente.fecha_registro.desc()).all()


def cambiar_estado_cliente(db: Session, id_cliente: int, nuevo_estado: str):

    cliente = db.query(Cliente).filter(
        Cliente.id_cliente == id_cliente
    ).first()

    if not cliente:
        return None

    cliente.estado_cliente = nuevo_estado
    db.commit()
    db.refresh(cliente)

    return cliente


def detalle_cliente(db: Session, id_cliente: int):

    cliente = db.query(Cliente).filter(
        Cliente.id_cliente == id_cliente
    ).first()

    if not cliente:
        return None

    total_ventas = db.query(Venta).filter(
        Venta.id_cliente == id_cliente
    ).count()

    total_suscripciones = db.query(Suscripcion).filter(
        Suscripcion.id_cliente == id_cliente
    ).count()

    total_pagos = db.query(Pago).filter(
        Pago.id_cliente == id_cliente
    ).count()

    total_licencias = db.query(Licencia)\
        .join(Venta, Licencia.id_venta == Venta.id_venta, isouter=True)\
        .filter(Venta.id_cliente == id_cliente)\
        .count()

    return {
        "cliente": cliente,
        "estadisticas": {
            "ventas": total_ventas,
            "suscripciones": total_suscripciones,
            "pagos": total_pagos,
            "licencias": total_licencias
        }
    }

def exportar_clientes_excel(db: Session):

    clientes = db.query(Cliente).all()

    wb = Workbook()
    ws = wb.active
    ws.title = "Clientes"

    # Encabezados
    ws.append([
        "ID",
        "Tipo",
        "Nombre / Empresa",
        "Documento",
        "Email",
        "Teléfono",
        "Estado",
        "Fecha Registro"
    ])

    for c in clientes:
        nombre = c.nombre_empresa if c.tipo_cliente == "empresa" else c.nombre_completo
        documento = c.ruc if c.tipo_cliente == "empresa" else c.dni

        ws.append([
            c.id_cliente,
            c.tipo_cliente,
            nombre,
            documento,
            c.email,
            c.telefono,
            c.estado_cliente,
            str(c.fecha_registro)
        ])

    file_stream = BytesIO()
    wb.save(file_stream)
    file_stream.seek(0)

    return file_stream