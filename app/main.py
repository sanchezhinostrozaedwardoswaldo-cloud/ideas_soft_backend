from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.connection import engine
from app.database.base import Base
from app.routers import auth_router, software_router, carrito_router, ventas_router, cliente_router


app = FastAPI(title="Ideas Soft API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],           # Permite que cualquier persona vea la demo
    allow_credentials=True,
    allow_methods=["*"],           # Permite OPTIONS (el error que tenía tu amigo)
    allow_headers=["*"],           # Permite enviar el Token Bearer
)

# Crear tablas si no existen
Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "Ideas Soft API Running"}

app.include_router(auth_router)

app.include_router(software_router)

app.include_router(carrito_router)

app.include_router(ventas_router)

app.include_router(cliente_router)