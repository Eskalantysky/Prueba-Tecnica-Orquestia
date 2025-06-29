from enum import Enum

class EstadoReserva(str, Enum):
    confirmada = "confirmada"
    completada = "completada"
    cancelada = "cancelada"

class EstadoMesa(str, Enum):
    libre = "libre"
    reservada = "reservada"
    ocupada = "ocupada"
