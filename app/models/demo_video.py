from sqlalchemy import Column, Integer, String, ForeignKey, Text
from app.database.base import Base

class DemoVideo(Base):
    __tablename__ = "demo_videos"

    id_video = Column(Integer, primary_key=True, autoincrement=True)
    id_software = Column(Integer, ForeignKey("software.id_software", ondelete="CASCADE"), nullable=False)
    titulo = Column(String(150))
    url = Column(String(255))
    descripcion = Column(Text)