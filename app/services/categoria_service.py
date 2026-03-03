from app.models.categoria import Categoria
from sqlalchemy.orm import Session


def get_all_categorias(db: Session):
    return db.query(Categoria)\
        .filter(Categoria.estado == "activo")\
        .all()


def create_categoria(db: Session, data):
    nueva = Categoria(
        nombre=data.nombre,
        descripcion=data.descripcion
    )
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva


def update_categoria(db: Session, id_categoria: int, data):
    categoria = db.query(Categoria).filter(
        Categoria.id_categoria == id_categoria
    ).first()

    if not categoria:
        return None

    categoria.nombre = data.nombre
    categoria.descripcion = data.descripcion
    db.commit()
    db.refresh(categoria)
    return categoria


def desactivar_categoria(db: Session, id_categoria: int):
    categoria = db.query(Categoria).filter(
        Categoria.id_categoria == id_categoria
    ).first()

    if not categoria:
        return None

    categoria.estado = "inactivo"
    db.commit()
    db.refresh(categoria)
    return categoria
