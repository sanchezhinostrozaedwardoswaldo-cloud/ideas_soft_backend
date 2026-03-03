from app.models.venta import Venta
from sqlalchemy.orm import Session
from app.models.suscripcion import Suscripcion
from app.models.licencia import Licencia
from app.models.pago import Pago


def obtener_compras_cliente(db: Session, id_cliente: int):
    return db.query(Venta)\
        .filter(Venta.id_cliente == id_cliente)\
        .order_by(Venta.fecha.desc())\
        .all()

def obtener_suscripciones_cliente(db: Session, id_cliente: int):
    return db.query(Suscripcion)\
        .filter(Suscripcion.id_cliente == id_cliente)\
        .order_by(Suscripcion.fecha_inicio.desc())\
        .all()

def obtener_licencias_cliente(db: Session, id_cliente: int):

    return db.query(Licencia)\
        .outerjoin(Venta, Licencia.id_venta == Venta.id_venta)\
        .outerjoin(Suscripcion, Licencia.id_suscripcion == Suscripcion.id_suscripcion)\
        .filter(
            (Venta.id_cliente == id_cliente) |
            (Suscripcion.id_cliente == id_cliente)
        )\
        .all()


def obtener_pagos_cliente(db: Session, id_cliente: int):
    return db.query(Pago)\
        .filter(Pago.id_cliente == id_cliente)\
        .order_by(Pago.fecha_pago.desc())\
        .all()