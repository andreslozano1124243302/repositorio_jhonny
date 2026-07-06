from fastapi import FastAPI
from routers import clientes, facturas, transacciones
from app.conexion_bd import crear_bd

app = FastAPI(title="API Andres")

@app.on_event("startup")
def on_startup():
    crear_bd()

app.include_router(clientes.router)
app.include_router(facturas.router)
app.include_router(transacciones.router)

@app.get("/")
def root():
    return {"mensaje": "API - Hola mundo"}