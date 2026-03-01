from sqlalchemy import text
from fastapi import HTTPException
from sqlalchemy.orm import Session


def completar_venta(db: Session, id_venta: int):

    try:
        result = db.execute(
            text("""
                UPDATE ventas
                SET estado = 'completada'
                WHERE id_venta = :id_venta
                RETURNING id_venta
            """),
            {"id_venta": id_venta}
        )

        venta_actualizada = result.scalar()

        if not venta_actualizada:
            raise HTTPException(
                status_code=404,
                detail="Venta no encontrada"
            )

        db.commit()

        return {
            "message": "Venta completada correctamente",
            "id_venta": venta_actualizada
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
