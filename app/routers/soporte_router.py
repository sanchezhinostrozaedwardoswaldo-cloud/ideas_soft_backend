from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.core.security import get_current_user
from app.models.usuario import Usuario
from app.services.soporte_service import (
    crear_ticket,
    obtener_mis_tickets,
    obtener_ticket_detalle,
    responder_ticket
)

router = APIRouter(prefix="/soporte", tags=["Soporte Cliente"])


@router.post("/tickets")
def crear(
    asunto: str,
    mensaje: str,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    return crear_ticket(db, current_user.id_cliente, asunto, mensaje)


@router.get("/mis-tickets")
def mis_tickets(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    return obtener_mis_tickets(db, current_user.id_cliente)


@router.get("/tickets/{id_ticket}")
def detalle(
    id_ticket: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    return obtener_ticket_detalle(db, id_ticket, current_user.id_cliente)


@router.post("/tickets/{id_ticket}/mensaje")
def responder(
    id_ticket: int,
    mensaje: str,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    return responder_ticket(db, id_ticket, current_user.id_usuario, mensaje)
