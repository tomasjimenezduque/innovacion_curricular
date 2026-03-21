from sqlalchemy.orm import Session
from .abstracciones.i_repository import IRepository
from models.aa_rc import AaRc  # Importamos tu modelo de SQLAlchemy

class AaRcRepository(IRepository):
    """
    Implementación del repositorio para Actividades Académicas - Registro Calificado.
    Se conecta a bdfacturas_postgres_local a través de SQLAlchemy.
    """

    def __init__(self, db: Session):
        """
        Recibe la sesión de la base de datos desde connection.py.
        """
        self.db = db

    def obtener_todos(self, esquema: str = None, limite: int = None):
        """Trae todos los registros de la tabla aa_rc."""
        query = self.db.query(AaRc)
        if limite:
            query = query.limit(limite)
        return query.all()

    def obtener_por_id(self, valor_id, esquema: str = None):
        """
        Obligatorio por interfaz, pero aa_rc usa llave compuesta.
        Retornamos None o podrías lanzar una excepción personalizada.
        """
        return None 

    def obtener_por_llave_compuesta(self, id_curso, cod_reg, esquema: str = None):
        """
        Busca usando la combinación de id_curso y codigo_registro.
        """
        return self.db.query(AaRc).filter(
            AaRc.id_curso == id_curso,
            AaRc.codigo_registro == cod_reg
        ).first()

    def guardar(self, entidad: AaRc, esquema: str = None):
        """Inserta o actualiza un registro."""
        try:
            self.db.add(entidad)
            self.db.commit()
            self.db.refresh(entidad)
            return True, "Registro guardado en innovacion_curricular"
        except Exception as e:
            self.db.rollback() # Si falla en Medellín, deshace los cambios
            return False, f"Error: {str(e)}"

    def eliminar(self, entidad: AaRc, esquema: str = None):
        """Borra el registro de la base de datos."""
        try:
            self.db.delete(entidad)
            self.db.commit()
            return True, "Registro eliminado correctamente"
        except Exception as e:
            self.db.rollback()
            return False, f"Error: {str(e)}"