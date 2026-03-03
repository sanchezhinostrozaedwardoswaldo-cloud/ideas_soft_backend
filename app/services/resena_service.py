from app.models.resena import Resena
from sqlalchemy.orm import Session


def crear_resena(db: Session, data, id_cliente: int):
    nueva = Resena(
        id_cliente=id_cliente,
        id_software=data.id_software,
        comentario=data.comentario,
        calificacion=data.calificacion
    )

    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva


def obtener_resenas_por_software(db: Session, id_software: int):
    return db.query(Resena)\
        .filter(
            Resena.id_software == id_software,
            Resena.estado == "visible"
        )\
        .all()


def cambiar_estado_resena(db: Session, id_resena: int, nuevo_estado: str):
    resena = db.query(Resena)\
        .filter(Resena.id_resena == id_resena)\
        .first()

    if not resena:
        return None

    resena.estado = nuevo_estado
    db.commit()
    db.refresh(resena)
    return resena
