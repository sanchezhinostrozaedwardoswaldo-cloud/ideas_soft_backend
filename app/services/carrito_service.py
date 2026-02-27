from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.carrito import Carrito
from app.models.carrito_detalle import CarritoDetalle
from app.models.software import Software
from app.schemas.carrito_schema import CarritoAgregar
from sqlalchemy import text


def agregar_al_carrito(db: Session, id_cliente: int, data):

    # 1 Verificar que el software exista y esté activo
    software = db.query(Software).filter(
        Software.id_software == data.id_software,
        Software.estado == "activo"
    ).first()

    if not software:
        raise HTTPException(status_code=404, detail="Software no disponible")

    # 2 Obtener o crear carrito activo del cliente
    carrito = db.query(Carrito).filter(
        Carrito.id_cliente == id_cliente,
        Carrito.estado == "activo"
    ).first()

    if not carrito:
        carrito = Carrito(id_cliente=id_cliente)
        db.add(carrito)
        db.commit()
        db.refresh(carrito)

    # 3 Verificar si ya existe el producto en el carrito
    detalle_existente = db.query(CarritoDetalle).filter(
        CarritoDetalle.id_carrito == carrito.id_carrito,
        CarritoDetalle.id_software == data.id_software,
        CarritoDetalle.tipo_operacion == data.tipo_operacion
    ).first()

    # 4 Determinar precio según tipo_operacion
    if data.tipo_operacion == "venta":
        precio = software.precio_venta
    else:
        precio = software.precio_alquiler

    if precio is None:
        raise HTTPException(status_code=400, detail="Precio no disponible para este tipo")

    # 5 Si existe → aumentar cantidad
    if detalle_existente:
        detalle_existente.cantidad += data.cantidad
    else:
        nuevo_detalle = CarritoDetalle(
            id_carrito=carrito.id_carrito,
            id_software=data.id_software,
            cantidad=data.cantidad,
            precio=precio,
            tipo_operacion=data.tipo_operacion
        )
        db.add(nuevo_detalle)

    db.commit()

    return {"message": "Producto agregado al carrito correctamente"}

def obtener_mi_carrito(db: Session, id_cliente: int):
    carrito = db.query(Carrito).filter(
        Carrito.id_cliente == id_cliente,
        Carrito.estado == "activo"
    ).first()

    if not carrito:
        return []

    return carrito.detalles

def eliminar_item_carrito(db: Session, id_cliente: int, id_detalle: int):
    detalle = db.query(CarritoDetalle).join(Carrito).filter(
        Carrito.id_cliente == id_cliente,
        CarritoDetalle.id_detalle == id_detalle
    ).first()

    if not detalle:
        raise Exception("Item no encontrado")

    db.delete(detalle)
    db.commit()

def convertir_carrito_en_venta(db: Session, id_cliente: int):

    carrito = db.query(Carrito).filter(
        Carrito.id_cliente == id_cliente,
        Carrito.estado == "activo"
    ).first()

    if not carrito:
        raise HTTPException(
            status_code=400,
            detail="No hay carrito activo para convertir"
        )

    try:
        db.execute(
            text("SELECT convertir_carrito_a_venta(:id_carrito)"),
            {"id_carrito": carrito.id_carrito}
        )

        db.commit()

        return {
            "message": "Carrito convertido en venta correctamente"
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))