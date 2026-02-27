from fastapi import FastAPI
from app.database.connection import engine
from app.database.base import Base
from app.routers import auth_router, software_router, carrito_router


app = FastAPI(title="Ideas Soft API")

# Crear tablas si no existen
Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "Ideas Soft API Running"}

app.include_router(auth_router)

app.include_router(software_router)

app.include_router(carrito_router)