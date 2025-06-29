from database import engine, Base, SessionLocal
from models import Mesa
from enums import EstadoMesa

def crear_datos_si_no_existen():
    # ✅ Crear las tablas si no existen antes de consultar
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    if db.query(Mesa).count() > 0:
        print("⚠️  Ya existen mesas en la base de datos. No se crearon nuevos datos.")
    else:
        mesas = [
            Mesa(nombre="Mesa 1", capacidad=2, estado=EstadoMesa.libre),
            Mesa(nombre="Mesa 2", capacidad=4, estado=EstadoMesa.libre),
            Mesa(nombre="Mesa 3", capacidad=6, estado=EstadoMesa.libre)
        ]
        db.add_all(mesas)
        db.commit()
        print("✅ Datos de prueba creados correctamente.")
    db.close()

def reiniciar_base_de_datos():
    confirmacion = input("⚠️ ¿Estás seguro de que quieres REINICIAR la base de datos? Esto eliminará TODOS los datos. (s/n): ").lower()
    if confirmacion == "s":
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)

        db = SessionLocal()
        mesas = [
            Mesa(nombre="Mesa 1", capacidad=2, estado=EstadoMesa.libre),
            Mesa(nombre="Mesa 2", capacidad=4, estado=EstadoMesa.libre),
            Mesa(nombre="Mesa 3", capacidad=6, estado=EstadoMesa.libre)
        ]
        db.add_all(mesas)
        db.commit()
        db.close()
        print("✅ Base de datos reiniciada con éxito.")
    else:
        print("❌ Reinicio cancelado.")

def mostrar_menu():
    while True:
        print("\n📋 MENÚ DE ADMINISTRACIÓN DE BASE DE DATOS")
        print("1. Crear datos de prueba")
        print("2. Reiniciar base de datos")
        print("3. Salir")

        opcion = input("Selecciona una opción (1/2/3): ").strip()

        if opcion == "1":
            crear_datos_si_no_existen()
        elif opcion == "2":
            reiniciar_base_de_datos()
        elif opcion == "3":
            print("👋 Saliendo del menú...")
            break
        else:
            print("❌ Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    mostrar_menu()
