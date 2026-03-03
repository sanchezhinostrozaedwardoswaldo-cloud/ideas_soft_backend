from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.soporte_ticket import SoporteTicket
from app.models.mensaje_ticket import MensajeTicket

# CLIENTE

def crear_ticket(db: Session, id_cliente: int, asunto: str, mensaje: str):

    nuevo_ticket = SoporteTicket(
        id_cliente=id_cliente,
        asunto=asunto,
        mensaje=mensaje,
        estado="abierto"
    )

    db.add(nuevo_ticket)
    db.commit()
    db.refresh(nuevo_ticket)

    return {
        "message": "Ticket creado correctamente",
        "id_ticket": nuevo_ticket.id_ticket
    }


def obtener_mis_tickets(db: Session, id_cliente: int):
    return db.query(SoporteTicket).filter(
        SoporteTicket.id_cliente == id_cliente
    ).order_by(SoporteTicket.fecha_creacion.desc()).all()


def obtener_ticket_detalle(db: Session, id_ticket: int, id_cliente: int):

    ticket = db.query(SoporteTicket).filter(
        SoporteTicket.id_ticket == id_ticket,
        SoporteTicket.id_cliente == id_cliente
    ).first()

    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket no encontrado")

    return ticket


def responder_ticket(db: Session, id_ticket: int, id_usuario: int, mensaje: str):

    ticket = db.query(SoporteTicket).filter(
        SoporteTicket.id_ticket == id_ticket
    ).first()

    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket no encontrado")

    nuevo_mensaje = MensajeTicket(
        id_ticket=id_ticket,
        id_usuario=id_usuario,
        mensaje=mensaje
    )

    if ticket.estado == "abierto":
        ticket.estado = "en_proceso"

    db.add(nuevo_mensaje)
    db.commit()

    return {"message": "Respuesta enviada correctamente"}


# ADMIN / SOPORTE

def obtener_todos_tickets(db: Session):
    return db.query(SoporteTicket).order_by(
        SoporteTicket.fecha_creacion.desc()
    ).all()


def cambiar_estado_ticket(db: Session, id_ticket: int, nuevo_estado: str):

    ticket = db.query(SoporteTicket).filter(
        SoporteTicket.id_ticket == id_ticket
    ).first()

    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket no encontrado")

    ticket.estado = nuevo_estado
    db.commit()

    return {"message": "Estado actualizado correctamente"}
