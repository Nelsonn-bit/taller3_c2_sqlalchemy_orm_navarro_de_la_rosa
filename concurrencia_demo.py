"""
Demostración de concurrencia: varios hilos agregan libros simultáneamente.
Se usa Lock para proteger la sección crítica (add + commit).
"""
import threading
from time import sleep
from threading import Lock
from sqlalchemy.exc import SQLAlchemyError
from modelo.libro import Libro, SessionLocal
from random import uniform

lock = Lock()


def agregar_concurrente(titulo: str, autor: str, precio: float, pausa: float = 0.1) -> None:
    """
    Inserta un libro con bloqueo para evitar conflictos de escritura simultánea.
    Cada hilo usa su propia sesión, garantizando independencia y cierre limpio.
    """
    session = SessionLocal()
    try:
        with lock:
            nuevo = Libro(titulo=titulo, autor=autor, precio=precio)
            session.add(nuevo)
            session.commit()
            print(f"[{threading.current_thread().name}] Agregado: {nuevo}")
            sleep(pausa)  # Simula variaciones de tiempo de trabajo
    except SQLAlchemyError as e:
        session.rollback()
        print(f"[{threading.current_thread().name}] Error. Rollback.")
        print("Detalle:", e)
    finally:
        session.close()


if __name__ == "__main__":
    hilos = []
    datos = [
        ("Refactoring", "Martin Fowler", 50.0),
        ("Clean Architecture", "Robert C. Martin", 48.0),
        ("Design Patterns", "GoF", 60.0),
        ("The Pragmatic Programmer", "Hunt & Thomas", 44.0),
        ("Effective Python", "Brett Slatkin", 42.0),
    ]

    for i, (t, a, p) in enumerate(datos, start=1):
        pausa = round(uniform(0.05, 0.2), 3)
        h = threading.Thread(
            target=agregar_concurrente,
            name=f"Hilo-{i}",
            args=(t, a, p, pausa)
        )
        hilos.append(h)
        h.start()

    for h in hilos:
        h.join()
