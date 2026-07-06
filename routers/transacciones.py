from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.modelos.Transacciones import Transaccion, TransaccionCrear, TransaccionRead # <--- IMPORTANTE: Importa TransaccionRead
from app.conexion_bd import get_session
from app.modelos.Facturas import Factura # Asegúrate de que esta ruta sea la correcta

router = APIRouter()

@router.get("/", response_model=list[TransaccionRead])
def listar_transacciones(session: Session = Depends(get_session)):
    transacciones = session.exec(select(Transaccion)).all()
    resultado = []
    
    # Creamos un TransaccionRead por cada registro y calculamos el total aquí
    for t in transacciones:
        total_calculado = t.cantidad * t.valor_unitario
        resultado.append(
            TransaccionRead(
                id=t.id,
                factura_id=t.factura_id,
                cantidad=t.cantidad,
                valor_unitario=t.valor_unitario,
                descripcion=t.descripcion,
                total=total_calculado
            )
        )
    return resultado

@router.post("/", response_model=TransaccionRead)
def crear_transaccion(datos_transaccion: TransaccionCrear, session: Session = Depends(get_session)):
    factura = session.get(Factura, datos_transaccion.factura_id)
    if not factura:
        raise HTTPException(status_code=404, detail="La factura no existe")

    transaccion = Transaccion.model_validate(datos_transaccion)
    session.add(transaccion)
    session.commit()
    session.refresh(transaccion)
    
    # Retornamos directamente el modelo de lectura con el cálculo
    total_calculado = transaccion.cantidad * transaccion.valor_unitario
    return TransaccionRead(
        id=transaccion.id,
        factura_id=transaccion.factura_id,
        cantidad=transaccion.cantidad,
        valor_unitario=transaccion.valor_unitario,
        descripcion=transaccion.descripcion,
        total=total_calculado
    )

@router.get("/{id}", response_model=TransaccionRead)
def obtener_transaccion(id: int, session: Session = Depends(get_session)):
    transaccion = session.get(Transaccion, id)
    if not transaccion:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")
    
    # Retornamos directamente el modelo de lectura
    total_calculado = transaccion.cantidad * transaccion.valor_unitario
    return TransaccionRead(
        id=transaccion.id,
        factura_id=transaccion.factura_id,
        cantidad=transaccion.cantidad,
        valor_unitario=transaccion.valor_unitario,
        descripcion=transaccion.descripcion,
        total=total_calculado
    )

@router.put("/{id}", response_model=TransaccionRead)
def actualizar_transaccion(id: int, datos_transaccion: TransaccionCrear, session: Session = Depends(get_session)):
    transaccion = session.get(Transaccion, id)
    if not transaccion:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")

    factura = session.get(Factura, datos_transaccion.factura_id)
    if not factura:
        raise HTTPException(status_code=404, detail="La factura no existe")

    transaccion.factura_id = datos_transaccion.factura_id
    transaccion.cantidad = datos_transaccion.cantidad
    transaccion.valor_unitario = datos_transaccion.valor_unitario
    transaccion.descripcion = datos_transaccion.descripcion

    session.add(transaccion)
    session.commit()
    session.refresh(transaccion)
    
    # Retornamos el modelo de lectura actualizado
    total_calculado = transaccion.cantidad * transaccion.valor_unitario
    return TransaccionRead(
        id=transaccion.id,
        factura_id=transaccion.factura_id,
        cantidad=transaccion.cantidad,
        valor_unitario=transaccion.valor_unitario,
        descripcion=transaccion.descripcion,
        total=total_calculado
    )

@router.delete("/{id}")
def eliminar_transaccion(id: int, session: Session = Depends(get_session)):
    transaccion = session.get(Transaccion, id)
    if not transaccion:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")
    session.delete(transaccion)
    session.commit()
    return {"mensaje": "Transacción eliminada correctamente"}