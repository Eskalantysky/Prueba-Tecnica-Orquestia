from pydantic import BaseModel
from datetime import datetime
from enums import EstadoReserva, EstadoMesa
from typing import Optional

class MesaBase(BaseModel):
    nombre: str
    capacidad: int

class MesaOut(MesaBase):
    id: int
    estado: EstadoMesa

    class Config:
        orm_mode = True

class MesaEstadoUpdate(BaseModel):
    estado: EstadoMesa

class ReservaBase(BaseModel):
    mesa_id: int
    fecha_hora_inicio: datetime
    fecha_hora_fin: datetime
    num_huespedes: int
    nombre_cliente: str

class ReservaCreate(BaseModel):
    mesa_id: int
    fecha: str  # formato YYYY-MM-DD
    hora: str   # formato HH:MM
    num_huespedes: int
    nombre_cliente: str

class ReservaOut(ReservaBase):
    id: int
    estado: EstadoReserva

    class Config:
        orm_mode = True

class DisponibilidadRequest(BaseModel):
    fecha: str  # formato "YYYY-MM-DD"
    hora: str   # formato "HH:MM"
    num_huespedes: int
