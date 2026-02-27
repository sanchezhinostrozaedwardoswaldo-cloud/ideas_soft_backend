from sqlalchemy.orm import Session
from app.models.software import Software
from app.schemas.software_schema import SoftwareCreate, SoftwareUpdate


def create_software(db: Session, data: SoftwareCreate):
    nuevo = Software(**data.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


def get_all_software(db: Session):
    return db.query(Software).filter(Software.estado == "activo").all()


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
