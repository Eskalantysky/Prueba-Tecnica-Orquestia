from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.orm import relationship
from database import Base
from enums import EstadoReserva, EstadoMesa
import enum

class Mesa(Base):
    __tablename__ = "mesas"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True)
    capacidad = Column(Integer)
    estado = Column(SqlEnum(EstadoMesa), default=EstadoMesa.libre, nullable=False)
    estados_temporales = relationship("EstadoMesaTemporal", back_populates="mesa")

# models.py

# class EstadoReserva(str, enum.Enum):
#     confirmada = "confirmada"
#     completada = "completada"
#     cancelada = "cancelada"

class Reserva(Base):
    __tablename__ = "reservas"

    id = Column(Integer, primary_key=True)
    mesa_id = Column(Integer, ForeignKey("mesas.id"))
    fecha_hora_inicio = Column(DateTime)
    fecha_hora_fin = Column(DateTime)
    num_huespedes = Column(Integer)
    nombre_cliente = Column(String)
    estado = Column(SqlEnum(EstadoReserva), default=EstadoReserva.confirmada, nullable=False)

    mesa = relationship("Mesa")

class EstadoMesaTemporal(Base):
    __tablename__ = "estado_mesa_temporal"
    id = Column(Integer, primary_key=True, index=True)
    mesa_id = Column(Integer, ForeignKey("mesas.id"))
    fecha_hora_inicio = Column(DateTime)
    fecha_hora_fin = Column(DateTime)

    mesa = relationship("Mesa", back_populates="estados_temporales")