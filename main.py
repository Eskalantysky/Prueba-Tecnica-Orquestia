from schemas import DisponibilidadRequest
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base
import crud, schemas
import models

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/mesas", response_model=list[schemas.MesaOut])
def listar_mesas(db: Session = Depends(get_db)):
    return crud.get_mesas(db)

@app.put("/mesas/{id_mesa}/estado", response_model=schemas.MesaOut)
def cambiar_estado_mesa(id_mesa: int, body: schemas.MesaEstadoUpdate, db: Session = Depends(get_db)):
    mesa = crud.update_estado_mesa(db, id_mesa, body.estado)
    if not mesa:
        raise HTTPException(status_code=404, detail="Mesa no encontrada")
    return mesa

@app.post("/reservas/disponibilidad")
def consultar_disponibilidad(payload: DisponibilidadRequest, db: Session = Depends(get_db)):
    from datetime import datetime, timedelta

    try:
        fecha_hora = datetime.strptime(f"{payload.fecha} {payload.hora}", "%Y-%m-%d %H:%M")
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato de fecha u hora inválido. Usa YYYY-MM-DD y HH:MM")

    mesas_disponibles = crud.verificar_disponibilidad(
        db=db,
        fecha_hora=fecha_hora,
        num_huespedes=payload.num_huespedes
    )

    return mesas_disponibles

@app.post("/reservas", response_model=schemas.ReservaOut)
def crear_reserva(body: schemas.ReservaCreate, db: Session = Depends(get_db)):
    return crud.crear_reserva(db, body)

@app.get("/reservas/{id_reserva}", response_model=schemas.ReservaOut)
def obtener_reserva(id_reserva: int, db: Session = Depends(get_db)):
    reserva = crud.get_reserva(db, id_reserva)
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    return reserva

@app.put("/reservas/{id_reserva}/cancelar", response_model=schemas.ReservaOut)
def cancelar_reserva(id_reserva: int, db: Session = Depends(get_db)):
    reserva = crud.cancelar_reserva(db, id_reserva)
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    return reserva

@app.get("/reservas", response_model=list[schemas.ReservaOut])
def obtener_todas_las_reservas(db: Session = Depends(get_db)):
    return db.query(models.Reserva).all()
