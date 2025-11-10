"""Modelos ORM: Categoria y Libro (relación uno-a-muchos)."""

from sqlalchemy import Column, Integer, String, Float, ForeignKey, create_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from pathlib import Path

DATA_DIR = Path("datos")
DATA_DIR.mkdir(exist_ok=True)
DB_URL = f"sqlite:///{(DATA_DIR / 'libros.db').as_posix()}"


Base = declarative_base()
engine = create_engine(DB_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


class Categoria(Base):
    """Representa una categoría de libros."""

    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), unique=True, nullable=False)

    libros = relationship("Libro", back_populates="categoria", cascade="all, delete-orphan")

    def __repr__(self) -> str:  # pragma: no cover
        return f"Categoria(id={self.id!r}, nombre={self.nombre!r})"


class Libro(Base):
    """Representa un libro perteneciente a una categoría."""

    __tablename__ = "libros"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(150), nullable=False)
    autor = Column(String(100), nullable=False)
    precio = Column(Float, nullable=False)
    categoria_id = Column(Integer, ForeignKey("categorias.id"), nullable=False)

    categoria = relationship("Categoria", back_populates="libros")

    def __repr__(self) -> str:  # pragma: no cover
        return (
            f"Libro(id={self.id!r}, titulo={self.titulo!r}, autor={self.autor!r}, "
            f"precio={self.precio!r}, categoria_id={self.categoria_id!r})"
        )


def init_db() -> None:
    """Crea las tablas si no existen."""
    Base.metadata.create_all(bind=engine)
