from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.core.security import require_role
from app.models.usuario import Usuario
from app.services.soporte_service import (
    obtener_todos_tickets,
    cambiar_estado_ticket,
    responder_ticket
)

router = APIRouter(prefix="/admin/tickets", tags=["Admin Tickets"])


@router.get("/")
def listar(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role(["admin", "soporte"]))
):
    return obtener_todos_tickets(db)


@router.patch("/{id_ticket}/estado")
def cambiar_estado(
    id_ticket: int,
    nuevo_estado: str,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role(["admin", "soporte"]))
):
    return cambiar_estado_ticket(db, id_ticket, nuevo_estado)


@router.post("/{id_ticket}/mensaje")
def responder_admin(
    id_ticket: int,
    mensaje: str,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role(["admin", "soporte"]))
):
    return responder_ticket(db, id_ticket, current_user.id_usuario, mensaje)
