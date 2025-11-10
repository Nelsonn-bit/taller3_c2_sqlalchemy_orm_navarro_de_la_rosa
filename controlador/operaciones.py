"""
Módulo: controlador.operaciones
Implementa operaciones CRUD y consultas sobre el modelo Libro.
Incluye manejo explícito de transacciones (commit/rollback) y cierres de sesión.
"""
from typing import Iterable, Optional
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select, update, delete
from modelo.libro import Libro, SessionLocal


def agregar(titulo: str, autor: str, precio: float) -> None:
    """Crea un libro y confirma la transacción."""
    session = SessionLocal()
    try:
        nuevo = Libro(titulo=titulo, autor=autor, precio=precio)
        session.add(nuevo)
        session.commit()  # Si algo falla, se capturará y se hará rollback
        print(f"Agregado: {nuevo}")
    except SQLAlchemyError as e:
        session.rollback()
        print("Error al agregar. Transacción revertida.")
        print("Detalle:", e)
    finally:
        session.close()


def listar() -> Iterable[Libro]:
    """Retorna todos los libros ordenados por id."""
    session = SessionLocal()
    try:
        stmt = select(Libro).order_by(Libro.id.asc())
        return session.scalars(stmt).all()
    finally:
        session.close()


def buscar_por_autor(autor: str) -> Iterable[Libro]:
    """Filtra libros por autor exacto."""
    session = SessionLocal()
    try:
        stmt = select(Libro).where(Libro.autor == autor).order_by(Libro.titulo.asc())
        return session.scalars(stmt).all()
    finally:
        session.close()


def actualizar_precio(titulo: str, nuevo_precio: float) -> bool:
    """
    Actualiza el precio del primer libro con ese título.
    Retorna True si se actualizó algún registro.
    """
    session = SessionLocal()
    try:
        stmt = (
            update(Libro)
            .where(Libro.titulo == titulo)
            .values(precio=nuevo_precio)
        )
        result = session.execute(stmt)
        session.commit()
        return result.rowcount > 0
    except SQLAlchemyError as e:
        session.rollback()
        print("Error en actualización. Transacción revertida.")
        print("Detalle:", e)
        return False
    finally:
        session.close()


def eliminar_por_titulo(titulo: str) -> int:
    """Elimina libros por título. Retorna la cantidad eliminada."""
    session = SessionLocal()
    try:
        stmt = delete(Libro).where(Libro.titulo == titulo)
        result = session.execute(stmt)
        session.commit()
        return result.rowcount or 0
    except SQLAlchemyError as e:
        session.rollback()
        print("Error en eliminación. Transacción revertida.")
        print("Detalle:", e)
        return 0
    finally:
        session.close()
