from sqlalchemy.orm import Session
from models import Mesa, Reserva, EstadoMesaTemporal
from schemas import ReservaCreate
from datetime import timedelta, datetime
from zoneinfo import ZoneInfo 
from enums import EstadoReserva, EstadoMesa
from sqlalchemy import and_
from fastapi import HTTPException


def get_mesas(db: Session):
    ahora = datetime.now(ZoneInfo("America/Bogota"))  # o tu zona local real
    mesas = db.query(Mesa).all()
    resultado = []

    for mesa in mesas:
        bloque_activo = db.query(EstadoMesaTemporal).filter(
            EstadoMesaTemporal.mesa_id == mesa.id,
            EstadoMesaTemporal.fecha_hora_inicio <= ahora,
            EstadoMesaTemporal.fecha_hora_fin > ahora
        ).first()

        estado = "ocupada" if bloque_activo else "libre"

        resultado.append({
            "id": mesa.id,
            "nombre": mesa.nombre,
            "capacidad": mesa.capacidad,
            "estado": estado
        })

    return resultado


def update_estado_mesa(db: Session, mesa_id: int, nuevo_estado: EstadoMesa):
    mesa = db.query(Mesa).filter(Mesa.id == mesa_id).first()
    if not mesa:
        raise HTTPException(status_code=404, detail="Mesa no encontrada")
    
    mesa.estado = nuevo_estado
    db.commit()
    db.refresh(mesa)
    return mesa


def verificar_disponibilidad(db: Session, fecha_hora: datetime, num_huespedes: int):
    inicio = fecha_hora
    fin = fecha_hora + timedelta(hours=2)

    mesas = db.query(Mesa).filter(Mesa.capacidad >= num_huespedes).all()
    disponibles = []

    for mesa in mesas:
        reservas_conflictivas = db.query(Reserva).filter(
            and_(
                Reserva.mesa_id == mesa.id,
                Reserva.estado == EstadoReserva.confirmada,
                Reserva.fecha_hora_inicio < fin,
                Reserva.fecha_hora_fin > inicio
            )
        ).all()

        if not reservas_conflictivas:
            disponibles.append(mesa)

    return disponibles


def crear_reserva(db: Session, reserva: ReservaCreate):
    # 1. Parsear fecha y hora
    try:
        fecha_hora_inicio = datetime.strptime(f"{reserva.fecha} {reserva.hora}", "%Y-%m-%d %H:%M")
    except ValueError:
        raise ValueError("Formato de fecha u hora inválido. Usa YYYY-MM-DD y HH:MM")

    fecha_hora_fin = fecha_hora_inicio + timedelta(hours=2)

    # 2. Verificar que la mesa exista
    mesa = db.query(Mesa).filter(Mesa.id == reserva.mesa_id).first()
    if not mesa:
        raise Exception("La mesa especificada no existe.")

    # 3. Verificar que la capacidad sea suficiente
    if reserva.num_huespedes > mesa.capacidad:
        raise Exception("La mesa no tiene capacidad suficiente para la cantidad de huéspedes.")

    # 4. Verificar que no haya conflictos con reservas existentes
    conflicto = db.query(Reserva).filter(
        and_(
            Reserva.mesa_id == reserva.mesa_id,
            Reserva.estado == EstadoReserva.confirmada,
            Reserva.fecha_hora_inicio < fecha_hora_fin,
            Reserva.fecha_hora_fin > fecha_hora_inicio
        )
    ).first()

    if conflicto:
        raise HTTPException(status_code=400, detail="La mesa ya está reservada en ese horario.")

    # 5. Crear la reserva
    nueva_reserva = Reserva(
        mesa_id=reserva.mesa_id,
        fecha_hora_inicio=fecha_hora_inicio,
        fecha_hora_fin=fecha_hora_fin,
        num_huespedes=reserva.num_huespedes,
        nombre_cliente=reserva.nombre_cliente,
        estado=EstadoReserva.confirmada
    )

    db.add(nueva_reserva)
    db.commit()
    db.refresh(nueva_reserva)

    return nueva_reserva

def get_reserva(db: Session, reserva_id: int):
    return db.query(Reserva).filter(Reserva.id == reserva_id).first()


def cancelar_reserva(db: Session, reserva_id: int):
    reserva = db.query(Reserva).filter(Reserva.id == reserva_id).first()
    if reserva:
        reserva.estado = EstadoReserva.cancelada

        # Liberar la mesa si la reserva estaba activa
        mesa = db.query(Mesa).filter(Mesa.id == reserva.mesa_id).first()
        if mesa:
            mesa.estado = EstadoMesa.libre
            db.add(mesa)

        db.commit()
        db.refresh(reserva)
    return reserva
