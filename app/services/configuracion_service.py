from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.configuracion_sistema import ConfiguracionSistema


# Obtener todas las configuraciones
def obtener_configuracion(db: Session):
    configuraciones = db.query(ConfiguracionSistema).all()

    return {
        config.clave: config.valor
        for config in configuraciones
    }


# Actualizar configuración por clave
def actualizar_configuracion(db: Session, clave: str, nuevo_valor: str):

    config = db.query(ConfiguracionSistema).filter(
        ConfiguracionSistema.clave == clave
    ).first()

    if not config:
        raise HTTPException(
            status_code=404,
            detail="Configuración no encontrada"
        )

    config.valor = nuevo_valor
    db.commit()

    return {
        "message": f"Configuración '{clave}' actualizada correctamente"
    }
