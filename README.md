# API RESTful para Gestión de Mesas y Reservas

##  Descripción del Proyecto

Esta es una **API RESTful desarrollada en Python utilizando FastAPI**, orientada a la **gestión de mesas y reservas en un restaurante**. El proyecto fue diseñado para cumplir con una prueba técnica, enfocándose en una arquitectura limpia, modularidad, buenas prácticas y visión de producto.

---

## Funcionalidades Principales

| Endpoint                             | Método | Descripción                                                                 |
|--------------------------------------|--------|-----------------------------------------------------------------------------|
| `/mesas`                             | GET    | Lista todas las mesas, su capacidad y estado actual (libre u ocupada).     |
| `/mesas/{id_mesa}/estado`            | PUT    | Actualiza el estado de una mesa (requiere API Key).                        |
| `/reservas/disponibilidad`          | POST   | Consulta qué mesas están disponibles en una fecha y hora específicas.      |
| `/reservas`                          | POST   | Crea una reserva nueva para una mesa (requiere API Key).                   |
| `/reservas/{id_reserva}`            | GET    | Consulta los detalles de una reserva.                                      |
| `/reservas/{id_reserva}/cancelar`   | PUT    | Cancela una reserva (requiere API Key).                                    |
| `/reservas`                          | GET    | Lista todas las reservas.                                                  |

---

## Arquitectura del Proyecto

```
├── main.py         ← Archivo principal con la definición de rutas
├── crud.py         ← Lógica de negocio y funciones CRUD
├── models.py       ← Modelos SQLAlchemy (ORM)
├── schemas.py      ← Modelos Pydantic para validación y serialización
├── enums.py        ← Definición de Enums personalizados
├── database.py     ← Conexión y configuración de SQLite con SQLAlchemy
├── security.py     ← Middleware de protección con API Key
├── init_db.py      ← Script para crear y poblar la base de datos
└── README.md       ← Documentación completa del proyecto
```


---

## Seguridad: API Key

Los endpoints que modifican datos (PUT y POST) requieren autenticación mediante una **API Key**.

- Header requerido:
X-API-Key: TU_API_KEY

- Valor sugerido para pruebas:
X-API-Key: Clave_OrquestIA


La clave se valida mediante un `Depends()` personalizado en `security.py`.

---

## Base de Datos

Se usa **SQLite** con SQLAlchemy como ORM.

Tablas:

- `mesas`: información de mesas disponibles
- `reservas`: reservas realizadas por clientes
- `estado_mesa_temporal`: bloqueos temporales por reserva activa

---

## Pruebas con Postman

Para probar los endpoints protegidos:

1. Establece el método `POST`, `PUT`, etc.
2. En la sección `Headers`, agrega:

Key: X-API-Key
Value: Clave_OrquestIA

3. Usa el cuerpo (`Body`) en formato `raw > JSON` como:

```json
{
  "fecha": "2025-06-30",
  "hora": "19:00",
  "num_huespedes": 2
}
```


---
## Requisitos Técnicos

- Python 3.10+
- FastAPI
- SQLAlchemy
- Pydantic
- Uvicorn
- n8n (Cloud o local)
---
## Autor

Andrés Escalante
Desarrollador Backend | Ingeniero de Datos
```
[GitHub: @Eskalantysky](https://github.com/Eskalantysky)
[LinkedIn: Andrés Escalante](https://www.linkedin.com/in/andr%C3%A9s-felipe-escalante-quintero-99721420b/)
```
