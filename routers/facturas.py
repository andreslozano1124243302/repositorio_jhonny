from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from datetime import date
from typing import List, Optional

from app.conexion_bd import get_session
from app.modelos.Facturas import Factura, FacturaCrear
from app.modelos.Clientes import Cliente

# --- ESQUEMAS LIMPIOS PARA MOSTRAR LA INFORMACIÓN ANIDADA ---
from sqlmodel import SQLModel

class TransaccionEnFactura(SQLModel):
    id: int
    cantidad: int
    valor_unitario: float
    descripcion: Optional[str] = None

class ClienteEnFactura(SQLModel):
    id: int
    nombre: str
    edad: int

class FacturaConDetalles(SQLModel):
    id: int
    fecha: date
    cliente_id: int
    monto: float
    descripcion: Optional[str] = None
    cliente: Optional[ClienteEnFactura] = None
    transacciones: List[TransaccionEnFactura] = []
# ------------------------------------------------------------

router = APIRouter(
    prefix="/facturas",
    tags=["Facturas"]
)

@router.get("/", response_model=list[FacturaConDetalles])
def listar_facturas(session: Session = Depends(get_session)):
    return session.exec(select(Factura)).all()

@router.post("/", response_model=Factura)
def crear_factura(datos_factura: FacturaCrear, session: Session = Depends(get_session)):
    cliente = session.get(Cliente, datos_factura.cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="El cliente no existe")

    factura = Factura.model_validate(datos_factura)
    session.add(factura)
    session.commit()
    session.refresh(factura)
    return factura

@router.get("/{id}", response_model=FacturaConDetalles)
def obtener_factura(id: int, session: Session = Depends(get_session)):
    factura = session.get(Factura, id)
    if not factura:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    return factura

@router.put("/{id}", response_model=Factura)
def actualizar_factura(id: int, datos_factura: FacturaCrear, session: Session = Depends(get_session)):
    factura = session.get(Factura, id)
    if not factura:
        raise HTTPException(status_code=404, detail="Factura no encontrada")

    cliente = session.get(Cliente, datos_factura.cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="El cliente no existe")

    factura.cliente_id = datos_factura.cliente_id
    factura.monto = datos_factura.monto
    factura.descripcion = datos_factura.descripcion

    session.add(factura)
    session.commit()
    session.refresh(factura)
    return factura

@router.delete("/{id}")
def eliminar_factura(id: int, session: Session = Depends(get_session)):
    factura = session.get(Factura, id)
    if not factura:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    session.delete(factura)
    session.commit()
    return {"mensaje": "Factura eliminada correctamente"}