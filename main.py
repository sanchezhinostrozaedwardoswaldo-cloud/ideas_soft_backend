import os
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv

# 1. Cargar configuración y variables de entorno
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    print("❌ ERROR: No se encontró DATABASE_URL en el archivo .env")

# 2. Configuración de SQLAlchemy
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 3. Modelo de la tabla Clientes (Directo en este archivo)
class Cliente(Base):
    __tablename__ = "clientes"

    id_cliente = Column(Integer, primary_key=True, index=True)
    tipo_cliente = Column(String(20), nullable=False)
    nombre_empresa = Column(String(150))
    ruc = Column(String(20), unique=True)
    nombre_completo = Column(String(150))
    dni = Column(String(15), unique=True)
    direccion = Column(String(200))
    telefono = Column(String(20), nullable=False)
    email = Column(String(150), nullable=False, unique=True)

    __table_args__ = (
        CheckConstraint("tipo_cliente IN ('empresa','persona_natural')", name="ck_clientes_tipo"),
    )

# 4. Inicializar FastAPI
app = FastAPI(title="Ideas Soft API Single File")

# Dependencia para la sesión de DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 5. Rutas (Endpoints)
@app.get("/")
def inicio():
    return {"mensaje": "API de Ideas Soft activa y conectada"}

@app.get("/clientes")
def listar_clientes(db: Session = Depends(get_db)):
    try:
        # Esto consulta la tabla clientes en Supabase
        clientes = db.query(Cliente).all()
        return clientes
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al conectar con la DB: {str(e)}")