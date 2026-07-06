# API Andres - Sistema de Facturación

API REST desarrollada con FastAPI y SQLModel para gestión de clientes, facturas y transacciones.

## Instalación

```bash
pip install -r requirements.txt
```

## Ejecución

```bash
python -m uvicorn main:app --reload
```

## Endpoints

- `/clientes` - Gestión de clientes
- `/facturas` - Gestión de facturas
- `/transacciones` - Gestión de transacciones

## Calcular Total de Facturas

```bash
python calcular_total_facturas.py