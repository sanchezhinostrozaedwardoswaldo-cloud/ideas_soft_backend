from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.models.demo_video import DemoVideo

router = APIRouter(prefix="/demo_videos", tags=["Videos de Demostración"])

@router.get("/")
def listar_videos(db: Session = Depends(get_db)):
    # Esto devuelve: id_video, id_software, titulo, url, descripcion
    return db.query(DemoVideo).all()