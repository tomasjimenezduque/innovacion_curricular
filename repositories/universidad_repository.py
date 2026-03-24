from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select, update
from .abstracciones.i_repository import IRepository
from models.universidad import Universidad

class UniversidadRepository(IRepository):

    def __init__(self, db: Session):
        self.db = db

    async def obtener_todos(self, esquema: str = None, limite: int = None):
        """Lista todas las universidades registradas."""
        stmt = select(Universidad)
        if limite:
            stmt = stmt.limit(limite)
        
        result = self.db.execute(stmt)
        return result.scalars().all()

    async def obtener_por_id(self, valor_id: int, esquema: str = None):
        """
        Obtiene una universidad y sus facultades asociadas.
        Ideal para vistas jerárquicas en la plataforma.
        """
        stmt = select(Universidad).where(Universidad.id == valor_id).options(
            joinedload(Universidad.facultad)
        )
        result = self.db.execute(stmt)
        return result.scalars().first()

    async def guardar(self, entidad: Universidad, esquema: str = None):
        try:
            self.db.add(entidad)
            self.db.commit()
            self.db.refresh(entidad)
            return True, "Universidad guardada correctamente"
        except Exception as e:
            self.db.rollback()
            return False, f"Error: {str(e)}"

    async def actualizar(self, valor_id: int, datos: dict, esquema: str = None):
        """
        Actualiza los datos de la institución.
        'datos' contiene los campos a modificar (ej. dirección, rector).
        """
        try:
            stmt = (
                update(Universidad)
                .where(Universidad.id == valor_id)
                .values(**datos)
            )
            result = self.db.execute(stmt)
            self.db.commit()
            
            if result.rowcount > 0:
                return True, "Universidad actualizada con éxito"
            return False, "No se encontró la universidad para actualizar"
        except Exception as e:
            self.db.rollback()
            return False, f"Error al actualizar: {str(e)}"

    async def eliminar(self, entidad: Universidad, esquema: str = None):
        try:
            self.db.delete(entidad)
            self.db.commit()
            return True, "Universidad eliminada correctamente"
        except Exception as e:
            self.db.rollback()
            return False, f"Error: {str(e)}"