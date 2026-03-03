from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.schemas.software_schema import SoftwareCreate, SoftwareUpdate, SoftwareResponse
from app.services.software_service import (
    create_software,
    get_all_software,
    get_software_by_id,
    update_software
)
from app.core.security import require_role
from app.models.usuario import Usuario
from typing import Optional
from fastapi import Query


router = APIRouter(prefix="/software", tags=["Software"])


@router.post("/", response_model=SoftwareResponse)
def crear(data: SoftwareCreate, db: Session = Depends(get_db),current_user: Usuario = Depends(require_role("admin"))):
    return create_software(db, data)


@router.get("/", response_model=list[SoftwareResponse])
def listar(
    categoria: Optional[int] = None,
    tipo: Optional[str] = Query(None, pattern="^(venta|suscripcion)$"),
    buscar: Optional[str] = None,
    orden: Optional[str] = None,
    db: Session = Depends(get_db)
):
    return get_all_software(
        db=db,
        categoria=categoria,
        tipo=tipo,
        buscar=buscar,
        orden=orden
    )


@router.get("/{id_software}", response_model=SoftwareResponse)
def detalle(id_software: int, db: Session = Depends(get_db)):
    software = get_software_by_id(db, id_software)
    if not software:
        raise HTTPException(status_code=404, detail="Software no encontrado")
    return software


@router.put("/{id_software}", response_model=SoftwareResponse)
def actualizar(id_software: int, data: SoftwareUpdate, db: Session = Depends(get_db), current_user: Usuario = Depends(require_role("admin"))):
    software = update_software(db, id_software, data)
    if not software:
        raise HTTPException(status_code=404, detail="Software no encontrado")
    return software

@router.patch("/{id_software}/desactivar", response_model=SoftwareResponse)
def desactivar(
    id_software: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role("admin"))
):
    software = get_software_by_id(db, id_software)

    if not software:
        raise HTTPException(status_code=404, detail="Software no encontrado")

    software.estado = "inactivo"
    db.commit()
    db.refresh(software)

    return software
