from sqlalchemy.orm import Session
from sqlalchemy import select, update
from .abstracciones.i_repository import IRepository
from models.premio import Premio

class PremioRepository(IRepository):

    def __init__(self, db: Session):
        self.db = db

    async def obtener_todos(self, esquema: str = None, limite: int = None):
        """Consulta asíncrona de todos los premios registrados."""
        stmt = select(Premio)
        if limite:
            stmt = stmt.limit(limite)
        
        result = self.db.execute(stmt)
        return result.scalars().all()

    async def obtener_por_id(self, valor_id: int, esquema: str = None):
        """Obtiene un premio específico por su identificador único."""
        stmt = select(Premio).where(Premio.id == valor_id)
        result = self.db.execute(stmt)
        return result.scalars().first()

    async def guardar(self, entidad: Premio, esquema: str = None):
        try:
            self.db.add(entidad)
            self.db.commit()
            self.db.refresh(entidad)
            return True, "Premio guardado correctamente"
        except Exception as e:
            self.db.rollback()
            return False, f"Error: {str(e)}"

    async def actualizar(self, valor_id: int, datos: dict, esquema: str = None):
        """
        Actualiza los datos de un premio (nombre, fecha, institución, etc.).
        'datos' es un diccionario con los campos a modificar.
        """
        try:
            stmt = (
                update(Premio)
                .where(Premio.id == valor_id)
                .values(**datos)
            )
            
            result = self.db.execute(stmt)
            self.db.commit()
            
            if result.rowcount > 0:
                return True, "Premio actualizado correctamente"
            return False, "No se encontró el premio para actualizar"
        except Exception as e:
            self.db.rollback()
            return False, f"Error al actualizar premio: {str(e)}"

    async def eliminar(self, entidad: Premio, esquema: str = None):
        try:
            self.db.delete(entidad)
            self.db.commit()
            return True, "Registro eliminado correctamente"
        except Exception as e:
            self.db.rollback()
            return False, f"Error: {str(e)}"