"""
Demostración de concurrencia: varios hilos agregan libros simultáneamente.
Se usa Lock para proteger la sección crítica (add + commit).
Compatible con el modelo Libro actual.
"""

import threading
from time import sleep
from threading import Lock
from random import uniform
from sqlalchemy.exc import SQLAlchemyError
from modelo.libro import Libro, SessionLocal, Base, engine

# 🔧 Asegura que la base y las tablas existan
Base.metadata.create_all(bind=engine)

lock = Lock()


def agregar_concurrente(titulo: str, autor: str, precio: float, categoria_id: int, pausa: float = 0.1) -> None:
    """Inserta un libro con bloqueo para evitar conflictos de escritura simultánea."""
    session = SessionLocal()
    try:
        with lock:
            nuevo = Libro(
                titulo=titulo,
                autor=autor,
                precio=precio,
                categoria_id=categoria_id,
            )
            session.add(nuevo)
            session.commit()
            print(f"[{threading.current_thread().name}] Agregado: {nuevo}")

        # Simula una pequeña espera aleatoria
        sleep(pausa)

    except SQLAlchemyError as e:
        session.rollback()
        print(f"[{threading.current_thread().name}] Error. Rollback ejecutado.")
        print("Detalle:", e)
    finally:
        session.close()


if __name__ == "__main__":
    print("=== Inicio de inserción concurrente ===")

    datos = [
        ("Refactoring", "Martin Fowler", 50.0, 1),
        ("Clean Architecture", "Robert C. Martin", 48.0, 1),
        ("Design Patterns", "GoF", 60.0, 1),
        ("The Pragmatic Programmer", "Hunt & Thomas", 44.0, 1),
        ("Effective Python", "Brett Slatkin", 42.0, 1),
    ]

    hilos = []
    for i, (t, a, p, cat) in enumerate(datos, start=1):
        pausa = round(uniform(0.05, 0.2), 3)
        h = threading.Thread(
            target=agregar_concurrente,
            name=f"Hilo-{i}",
            args=(t, a, p, cat, pausa),
        )
        hilos.append(h)
        h.start()

    for h in hilos:
        h.join()

    print("\n=== Inserciones completadas ===")

    # Verificar los libros insertados
    session = SessionLocal()
    libros = session.query(Libro).all()
    print("\n Libros insertados:")
    for libro in libros:
        print(libro)
    session.close()
