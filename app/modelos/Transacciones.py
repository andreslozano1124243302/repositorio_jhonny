from typing import Optional
from sqlmodel import SQLModel, Field, Relationship

class Transaccion(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    factura_id: int = Field(foreign_key="factura.id") 
    cantidad: int  
    valor_unitario: float  
    descripcion: Optional[str] = None

    factura: Optional["Factura"] = Relationship(back_populates="transacciones")

class TransaccionCrear(SQLModel):
    factura_id: int
    cantidad: int
    valor_unitario: float
    descripcion: Optional[str] = None

# --- AGREGA ESTA NUEVA CLASE AQUÍ ABAJO ---
class TransaccionRead(SQLModel):
    id: int
    factura_id: int
    cantidad: int
    valor_unitario: float
    descripcion: Optional[str] = None
    total: float # <-- Aquí le avisamos a FastAPI que mostraremos el total