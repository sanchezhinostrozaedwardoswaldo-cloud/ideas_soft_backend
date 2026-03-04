from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.connection import engine
from app.database.base import Base
from app.routers import auth_router, software_router, carrito_router, cliente_router, categoria_router, resena_router, panel_router, admin_pago_router, admin_cliente_router, dashboard_router, soporte_router, admin_ticket_router, configuracion_router, usuarios_admin_router, video_router


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

app.include_router(cliente_router)

app.include_router(categoria_router)

app.include_router(resena_router)

app.include_router(panel_router)

app.include_router(admin_pago_router)

app.include_router(admin_cliente_router)

app.include_router(dashboard_router)

app.include_router(soporte_router)

app.include_router(admin_ticket_router)

app.include_router(configuracion_router)

app.include_router(usuarios_admin_router)

app.include_router(video_router)