from sqlalchemy.orm import Session
from fastapi import HTTPException
from passlib.context import CryptContext
from app.models.usuario import Usuario

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Listar usuarios internos (no clientes)
def listar_usuarios_internos(db: Session):
    return db.query(Usuario).filter(
        Usuario.id_cliente == None
    ).all()


# Crear usuario interno
def crear_usuario_interno(db: Session, email: str, password: str, rol: str):

    if rol not in ["admin", "contador", "soporte"]:
        raise HTTPException(status_code=400, detail="Rol inválido")

    usuario_existente = db.query(Usuario).filter(
        Usuario.email == email
    ).first()

    if usuario_existente:
        raise HTTPException(status_code=400, detail="El email ya está registrado")

    hashed_password = pwd_context.hash(password)

    nuevo_usuario = Usuario(
        email=email,
        password=hashed_password,
        rol=rol,
        estado="activo",
        id_cliente=None
    )

    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)

    return {"message": "Usuario interno creado correctamente"}


# Cambiar estado
def cambiar_estado_usuario(db: Session, id_usuario: int, nuevo_estado: str):

    if nuevo_estado not in ["activo", "inactivo"]:
        raise HTTPException(status_code=400, detail="Estado inválido")

    usuario = db.query(Usuario).filter(
        Usuario.id_usuario == id_usuario,
        Usuario.id_cliente == None
    ).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    usuario.estado = nuevo_estado
    db.commit()

    return {"message": "Estado actualizado correctamente"}


# Cambiar contraseña
def cambiar_password_usuario(db: Session, id_usuario: int, nueva_password: str):

    usuario = db.query(Usuario).filter(
        Usuario.id_usuario == id_usuario,
        Usuario.id_cliente == None
    ).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    usuario.password = pwd_context.hash(nueva_password)
    db.commit()

    return {"message": "Contraseña actualizada correctamente"}
