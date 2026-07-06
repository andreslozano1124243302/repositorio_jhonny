from sqlmodel import Session, text
from app.conexion_bd import engine

# Calcular el valor total de todas las facturas
def calcular_total_facturas():
    with Session(engine) as session:
        # Consulta SQL directa para sumar el campo monto
        result = session.exec(text("SELECT SUM(monto) FROM factura")).one()
        return result[0] if result[0] else 0

# Calcular el valor total por cliente
def calcular_total_por_cliente():
    with Session(engine) as session:
        # Consulta SQL para obtener el total por cliente
        result = session.exec(text("""
            SELECT c.nombre, SUM(f.monto) as total
            FROM cliente c
            JOIN factura f ON c.id = f.cliente_id
            GROUP BY c.id, c.nombre
        """)).all()
        return result

if __name__ == "__main__":
    total = calcular_total_facturas()
    print(f"Valor total de todas las facturas: {total}")
    print("\nDesglose por cliente:")
    print("-" * 40)
    for cliente in calcular_total_por_cliente():
        print(f"Cliente: {cliente[0]}, Total: {cliente[1]}")
