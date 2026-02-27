from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.schemas.usuario_schema import UsuarioCreate, UsuarioLogin, RegisterRequest
from app.services.auth_service import register_cliente_usuario, authenticate_user
from app.core.security import create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register")
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    return register_cliente_usuario(db, data)



@router.post("/login")
def login(user: UsuarioLogin, db: Session = Depends(get_db)):

    db_user = authenticate_user(db, user.email, user.password)

    if not db_user:
        return {"error": "Credenciales inválidas"}

    token = create_access_token({
        "sub": str(db_user.id_usuario),  
        "rol": db_user.rol,
        "id_cliente": db_user.id_cliente
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }

