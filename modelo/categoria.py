"""
Módulo: modelo.categoria
Define la clase ORM para la tabla 'categorias'.
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from modelo.libro import Base  # usa la misma Base de libro.py

class Categoria(Base):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False, unique=True)

    # Relación inversa con Libro
    libros = relationship("Libro", back_populates="categoria")

    def __repr__(self):
        return f"Categoria(id={self.id}, nombre='{self.nombre}')"
