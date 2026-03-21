# servicios/fabrica_repositorios.py
from connection import SessionLocal  # Importa tu generador de sesiones
from repositories.aa_rc_repository import AaRcRepository

def crear_servicio_aa_rc():
    """
    Fábrica que instancia el repositorio inyectándole la sesión de BD.
    Esto permite que el controlador no tenga que saber NADA de SQLAlchemy.
    """
    # 1. Creamos una sesión de base de datos
    db = SessionLocal()
    
    try:
        # 2. Creamos el repositorio y le "inyectamos" la sesión
        repositorio = AaRcRepository(db)
        return repositorio
    finally:
        # Nota: En una API real, la sesión se suele cerrar 
        # después de la respuesta, pero para probar tu lógica inicial,
        # esto permitirá que el controlador reciba el objeto.
        pass