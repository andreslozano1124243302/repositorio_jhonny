from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from datetime import date

class Factura(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    fecha: date  
    cliente_id: int = Field(foreign_key="cliente.id") 
    monto: float
    descripcion: Optional[str] = None

    # Relaciones: Una factura pertenece a un cliente y tiene muchas transacciones
    cliente: Optional["Cliente"] = Relationship(back_populates="facturas")
    transacciones: List["Transaccion"] = Relationship(back_populates="factura")

class FacturaCrear(SQLModel):
    fecha: date
    cliente_id: int
    monto: float
    descripcion: Optional[str] = None