from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

# Usa la URL de la base de datos desde las configuraciones
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# Crea el motor de la base de datos
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Crea una fábrica de sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crea una clase base para los modelos declarativos
Base = declarative_base()

def get_db():
    """
    Genera un generador de sesiones de base de datos.
    
    Yields:
        Session: Una sesión de base de datos.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()