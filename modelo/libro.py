"""
Módulo: modelo.libro
Define la clase ORM para la tabla 'libros' y configura la conexión a la base de datos.
Incluye la relación con Categoria (uno a muchos).
"""

from pathlib import Path
from sqlalchemy import Column, Integer, String, Float, ForeignKey, create_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

# === Configuración de la base de datos ===
DATA_DIR = Path("datos")
DATA_DIR.mkdir(exist_ok=True)

DB_URL = f"sqlite:///{(DATA_DIR / 'libros.db').as_posix()}"
engine = create_engine(DB_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

# === Clase base para los modelos ORM ===
Base = declarative_base()


# === Clase Libro ===
class Libro(Base):
    __tablename__ = "libros"

    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(200), nullable=False)
    autor = Column(String(100), nullable=False)
    precio = Column(Float, nullable=False)
    categoria_id = Column(Integer, ForeignKey("categorias.id"), nullable=False)

    # Relación con Categoria
    categoria = relationship("Categoria", back_populates="libros")

    def __repr__(self):
        return (f"Libro(id={self.id}, titulo='{self.titulo}', autor='{self.autor}', "
                f"precio={self.precio}, categoria_id={self.categoria_id})")
