from sqlalchemy.orm import Session
from app.models.software import Software
from app.schemas.software_schema import SoftwareCreate, SoftwareUpdate
from sqlalchemy import func, desc
from app.models.software import Software
from app.models.detalle_venta import DetalleVenta
from app.models.resena import Resena
from app.models.software_categoria import SoftwareCategoria

def create_software(db: Session, data: SoftwareCreate):
    nuevo = Software(**data.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


def get_all_software(db, categoria=None, tipo=None, buscar=None, orden=None):

    query = db.query(Software).filter(Software.estado == "activo")

    # 🔹 Filtro por categoría
    if categoria:
        query = query.join(SoftwareCategoria).filter(
            SoftwareCategoria.id_categoria == categoria
        )

    # 🔹 Filtro por tipo (venta o suscripción)
    if tipo == "venta":
        query = query.filter(Software.precio_venta.isnot(None))
    elif tipo == "suscripcion":
        query = query.filter(Software.precio_alquiler.isnot(None))

    # 🔹 Búsqueda parcial
    if buscar:
        query = query.filter(Software.nombre.ilike(f"%{buscar}%"))

    # 🔹 Ordenamiento
    if orden == "precio_asc":
        query = query.order_by(Software.precio_venta.asc())

    elif orden == "precio_desc":
        query = query.order_by(Software.precio_venta.desc())

    elif orden == "mas_vendidos":
        query = (
            query.outerjoin(DetalleVenta)
            .group_by(Software.id_software)
            .order_by(desc(func.sum(DetalleVenta.cantidad)))
        )

    elif orden == "mejor_calificados":
        query = (
            query.outerjoin(Resena)
            .group_by(Software.id_software)
            .order_by(desc(func.avg(Resena.calificacion)))
        )

    return query.all()


def get_software_by_id(db: Session, id_software: int):
    return db.query(Software).filter(Software.id_software == id_software, Software.estado == "activo").first()


def update_software(db: Session, id_software: int, data: SoftwareUpdate):
    software = get_software_by_id(db, id_software)
    if not software:
        return None

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(software, key, value)

    db.commit()
    db.refresh(software)
    return software
