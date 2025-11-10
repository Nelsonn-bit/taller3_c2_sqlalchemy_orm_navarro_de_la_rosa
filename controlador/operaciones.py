"""Operaciones CRUD y utilidades con transacciones seguras y concurrencia."""

from typing import Iterable, List, Optional
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select, update, delete
from threading import Lock
from modelo.libro import Libro, Categoria, SessionLocal, init_db

# Inicializar la base de datos al importar
init_db()

db_lock = Lock()


def crear_categoria(nombre: str) -> Optional[Categoria]:
    """Crea una categoría. Retorna la categoría o None si falla."""
    session = SessionLocal()
    try:
        cat = Categoria(nombre=nombre)
        session.add(cat)
        session.commit()
        session.refresh(cat)
        return cat
    except SQLAlchemyError:
        session.rollback()
        return None
    finally:
        session.close()


def listar_categorias() -> Iterable[Categoria]:
    """Retorna todas las categorías ordenadas por nombre."""
    session = SessionLocal()
    try:
        stmt = select(Categoria).order_by(Categoria.nombre.asc())
        return session.scalars(stmt).all()
    finally:
        session.close()


def agregar_libro(titulo: str, autor: str, precio: float, categoria_id: int) -> bool:
    """Agrega un libro asociado a categoria_id. Retorna True si OK."""
    session = SessionLocal()
    try:
        nuevo = Libro(titulo=titulo, autor=autor, precio=precio, categoria_id=categoria_id)
        session.add(nuevo)
        session.commit()
        return True
    except SQLAlchemyError:
        session.rollback()
        return False
    finally:
        session.close()


def listar_libros() -> Iterable[Libro]:
    """Retorna todos los libros ordenados por id."""
    session = SessionLocal()
    try:
        stmt = select(Libro).order_by(Libro.id.asc())
        return session.scalars(stmt).all()
    finally:
        session.close()


def buscar_por_categoria(categoria_nombre: str) -> List[Libro]:
    """Retorna libros que pertenecen a la categoría cuyo nombre exacto coincida."""
    session = SessionLocal()
    try:
        stmt = (
            select(Libro)
            .join(Categoria)
            .where(Categoria.nombre == categoria_nombre)
            .order_by(Libro.titulo.asc())
        )
        return session.scalars(stmt).all()
    finally:
        session.close()


def actualizar_precio(titulo: str, nuevo_precio: float) -> bool:
    """Actualiza el precio del primer libro con ese título. Retorna True si actualizó."""
    session = SessionLocal()
    try:
        stmt = update(Libro).where(Libro.titulo == titulo).values(precio=nuevo_precio)
        result = session.execute(stmt)
        session.commit()
        return result.rowcount > 0
    except SQLAlchemyError:
        session.rollback()
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
    except SQLAlchemyError:
        session.rollback()
        return 0
    finally:
        session.close()


def agregar_concurrente(titulo: str, autor: str, precio: float, categoria_id: int, lock: Lock = db_lock) -> bool:
    """
    Agrega un libro usando lock para proteger add+commit.
    Cada hilo usa su propia sesión; retorna True si OK.
    """
    session = SessionLocal()
    try:
        with lock:
            nuevo = Libro(titulo=titulo, autor=autor, precio=precio, categoria_id=categoria_id)
            session.add(nuevo)
            session.commit()
        return True
    except SQLAlchemyError:
        session.rollback()
        return False
    finally:
        session.close()
