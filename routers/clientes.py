from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select

from app.conexion_bd import get_session
from app.modelos.Clientes import Cliente, ClienteCrear

router = APIRouter(
    prefix="/clientes",
    tags=["Clientes"]
)


@router.get("/", response_model=list[Cliente])
def listar_clientes(session: Session = Depends(get_session)):
    clientes = session.exec(select(Cliente)).all() # Asegúrate de usar Cliente aquí
    return clientes


@router.post("/", response_model=Cliente)
def crear_cliente(datos_cliente: ClienteCrear, session: Session = Depends(get_session)):
    cliente = Cliente.model_validate(datos_cliente)

    session.add(cliente)
    session.commit()
    session.refresh(cliente)

    return cliente


@router.get("/{id}", response_model=Cliente)
def obtener_cliente(id: int, session: Session = Depends(get_session)):
    cliente = session.get(Cliente, id)

    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    return cliente


@router.put("/{id}", response_model=Cliente)
def actualizar_cliente(id: int, datos_cliente: ClienteCrear, session: Session = Depends(get_session)):
    cliente = session.get(Cliente, id)

    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    cliente.nombre = datos_cliente.nombre
    cliente.edad = datos_cliente.edad
    cliente.descripcion = datos_cliente.descripcion

    session.add(cliente)
    session.commit()
    session.refresh(cliente)

    return cliente


@router.delete("/{id}")
def eliminar_cliente(id: int, session: Session = Depends(get_session)):
    cliente = session.get(Cliente, id)

    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    session.delete(cliente)
    session.commit()

    return {"mensaje": "Cliente eliminado correctamente"}