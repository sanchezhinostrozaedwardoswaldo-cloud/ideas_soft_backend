from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy.sql import func
from app.models.cliente import Cliente
from app.models.usuario import Usuario
from app.core.security import hash_password, verify_password
from app.schemas.usuario_schema import RegisterRequest


def register_cliente_usuario(db: Session, data: RegisterRequest):

    # 1️⃣ Verificar si el email ya existe en usuarios
    existing_user = db.query(Usuario).filter(
        Usuario.email == data.email
    ).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email ya registrado")

    # 2️⃣ Crear cliente
    nuevo_cliente = Cliente(
        tipo_cliente=data.tipo_cliente,
        nombre_empresa=data.nombre_empresa,
        ruc=data.ruc,
        nombre_completo=data.nombre_completo,
        dni=data.dni,
        direccion=data.direccion,
        telefono=data.telefono,
        email=data.email
    )

    db.add(nuevo_cliente)
    db.commit()
    db.refresh(nuevo_cliente)

    # 3️⃣ Crear usuario vinculado al cliente
    nuevo_usuario = Usuario(
        id_cliente=nuevo_cliente.id_cliente,
        email=data.email,
        password=hash_password(data.password),
        rol="cliente",
        estado="activo"
    )

    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)

    return {
        "message": "Usuario registrado correctamente",
        "id_usuario": nuevo_usuario.id_usuario
    }


def authenticate_user(db: Session, email: str, password: str):

    user = db.query(Usuario).filter(
        Usuario.email == email,
        Usuario.estado == "activo"
    ).first()

    if not user:
        return None

    if not verify_password(password, user.password):
        return None

    user.ultimo_login = func.now()
    db.commit()

    return user
