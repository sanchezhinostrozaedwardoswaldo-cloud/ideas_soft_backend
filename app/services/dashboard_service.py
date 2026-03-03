from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.cliente import Cliente
from app.models.venta import Venta
from app.models.suscripcion import Suscripcion
from app.models.pago import Pago
from app.models.detalle_venta import DetalleVenta
from app.models.software import Software
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO


def resumen_general(db: Session):

    total_clientes = db.query(Cliente).count()

    total_ventas = db.query(Venta).count()

    ingresos_totales = db.query(
        func.coalesce(func.sum(Pago.monto), 0)
    ).filter(
        Pago.estado == "completado"
    ).scalar()

    suscripciones_activas = db.query(Suscripcion).filter(
        Suscripcion.estado == "activa"
    ).count()

    return {
        "total_clientes": total_clientes,
        "total_ventas": total_ventas,
        "ingresos_totales": float(ingresos_totales),
        "suscripciones_activas": suscripciones_activas
    }


def software_mas_vendido(db: Session):

    result = db.query(
        Software.nombre,
        func.sum(DetalleVenta.cantidad).label("total_vendido")
    ).join(
        DetalleVenta, Software.id_software == DetalleVenta.id_software
    ).group_by(
        Software.nombre
    ).order_by(
        func.sum(DetalleVenta.cantidad).desc()
    ).first()

    return result


def clientes_con_mas_compras(db: Session):

    result = db.query(
        Cliente.nombre_completo,
        func.count(Venta.id_venta).label("total_compras")
    ).join(
        Venta, Cliente.id_cliente == Venta.id_cliente
    ).group_by(
        Cliente.nombre_completo
    ).order_by(
        func.count(Venta.id_venta).desc()
    ).limit(5).all()

    return result

def generar_reporte_pdf(db: Session):

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer)
    elements = []

    styles = getSampleStyleSheet()
    elements.append(Paragraph("REPORTE GENERAL - IDEAS SOFT", styles["Title"]))
    elements.append(Spacer(1, 0.3 * inch))

    resumen = resumen_general(db)
    top_software = software_mas_vendido(db)
    top_clientes = clientes_con_mas_compras(db)

    data = [
        ["Total Clientes", resumen["total_clientes"]],
        ["Total Ventas", resumen["total_ventas"]],
        ["Ingresos Totales", resumen["ingresos_totales"]],
        ["Suscripciones Activas", resumen["suscripciones_activas"]],
    ]

    table = Table(data)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 0.5 * inch))

    if top_software:
        elements.append(Paragraph(
            f"Software más vendido: {top_software[0]} ({top_software[1]} unidades)",
            styles["Normal"]
        ))

    elements.append(Spacer(1, 0.3 * inch))

    elements.append(Paragraph("Top 5 Clientes:", styles["Heading2"]))
    elements.append(Spacer(1, 0.2 * inch))

    for c in top_clientes:
        elements.append(Paragraph(
            f"{c[0]} - {c[1]} compras",
            styles["Normal"]
        ))

    doc.build(elements)
    buffer.seek(0)

    return buffer