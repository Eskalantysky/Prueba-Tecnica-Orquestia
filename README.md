# API RESTful para Gestión de Mesas y Reservas

##  Descripción del Proyecto

Esta es una **API RESTful desarrollada en Python utilizando FastAPI**, orientada a la **gestión de mesas y reservas en un restaurante**. El proyecto fue diseñado para cumplir con una prueba técnica, enfocándose en una arquitectura limpia, modularidad, buenas prácticas y visión de producto.

---

## Instalación y Puesta en Marcha

1. Clonar el repositorio:

```
git clone https://github.com/Eskalantysky/Prueba-Tecnica-Orquestia.git
cd Prueba-Tecnica-Orquestia
```

2. Crear entorno virtual y activar:
```
python -m venv venv
venv\Scripts\activate  # En Windows
source venv/bin/activate  # En Linux/macOS
```

3. Instalar dependencias:
```
pip install -r requirements.txt
```

4. Inicializar la base de datos con datos de prueba:
Antes de Iniciar el servidor, es importante crear la bases de datos ejecutando init_db.py, para ejecutarlo inicia con el comando

```
python init_db.py
```

Luego de ejecutar el programa init_db.py le aparecerá un menú

Para crear la base de datos por primera vez presiona 1.

De otra forma, si desea reiniciar la base de datos presiona 2 y 3 para salir del menú.

5. Ejecutar el servidor FastAPI:
```
uvicorn main:app --reload
```

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

## Integración con n8n

Esta API fue integrada exitosamente con n8n, una plataforma de automatización de flujos, para demostrar visión de producto y facilidad de integración externa.

¿Qué hace el flujo?

1. Se activa a través de un Webhook que recibe un JSON con la siguiente estructura:

```json
{
  "fecha": "2025-06-30",
  "hora": "19:00",
  "num_huespedes": 2
}
```

2. El webhook activa el flujo de trabajo en n8n.

3. Luego, se realiza una petición HTTP POST al endpoint de esta API /reservas/disponibilidad.

4. El resultado (lista de mesas disponibles) es devuelto como respuesta del webhook.

## Estructura del Workflow en n8n

El flujo está compuesto por 3 nodos:

1. Webhook

- `Método`: POST

- `Path`: /consulta-mesas

- Recibe un JSON desde cualquier cliente externo.


2. HTTP Request

- `Método`: POST

- `URL`: La URL pública de tu API (ej. generada con ngrok)

- Recibe un JSON desde cualquier cliente externo. Ejemplo: https://abcd1234.ngrok.io/reservas/disponibilidad

- Body en formato JSON:

```json
{
  "fecha": "{{$json["body"]["fecha"]}}",
  "hora": "{{$json["body"]["hora"]}}",
  "num_huespedes": {{$json["body"]["num_huespedes"]}}
}
```

3. Respond to Webhook

- Devuelve como respuesta el resultado del nodo anterior.

- Cuerpo:
```json
{{$node["HTTP Request"].json}}
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

[GitHub: @Eskalantysky](https://github.com/Eskalantysky)

[LinkedIn: Andrés Escalante](https://www.linkedin.com/in/andr%C3%A9s-felipe-escalante-quintero-99721420b/)

