"""
Modúlo: modelo.libro
Define la clase ORM 'Libro' y configura 
la conexión a la base de datos.
"""


from pathlib import Path
from sqlalchemy import create_engine, Column, Integer, String , Float
from sqlalchemy.orm import declarative_base, sessionmaker


# 1) Declarative Base : clase base para los modelos ORM

Base = declarative_base()

# 2) Ruta de base de datos ( fuera del có digo fuente )

DATA_DIR = Path("datos")
DATA_DIR.mkdir(exist_ok=True)
DB_URL = f"sqlite:///{DATA_DIR / 'libros.db'}.as_posix()"

# 3) Motor de base de datos: echo=True muestra el SQL generado por el ORM
engine = create_engine(DB_URL, echo=True, future=True)

# 4) Fabricante de sesiones: cada operación ORM usa su propia sesión
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


class Libro(Base):
    """
    Clase ORM que representa la tabla 'libros'.
    - id: clave primaria autoincremental
    - titulo: texto no nulo
    - autor: texto no nulo
    - precio: valor numérico (float) no nulo
    """

    __tablename__ = "libros"

    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String, nullable=False)
    autor = Column(String, nullable=False)
    precio = Column(Float, nullable=False)

    def __repr__(self) -> str:
        return f"<Libro id={self.id} titulo='{self.titulo}' autor='{self.autor}' precio={self.precio:.2f}>"

# 5) Crear las tablas (si no existen)
Base.metadata.create_all(engine)
