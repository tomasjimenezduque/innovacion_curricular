from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select, update
from .abstracciones.i_repository import IRepository
from models.programa import Programa

class ProgramaRepository(IRepository):

    def __init__(self, db: Session):
        self.db = db

    async def obtener_todos(self, esquema: str = None, limite: int = None):
        """
        Obtiene todos los programas cargando solo la facultad para optimizar.
        """
        stmt = select(Programa).options(joinedload(Programa.facultad_))
        if limite:
            stmt = stmt.limit(limite)
        
        result = self.db.execute(stmt)
        return result.scalars().all()

    async def obtener_por_id(self, valor_id: int, esquema: str = None):
        """
        Carga el programa con sus relaciones Many-to-Many (Áreas e Innovación).
        """
        stmt = (
            select(Programa)
            .where(Programa.id == valor_id)
            .options(
                joinedload(Programa.facultad_),
                joinedload(Programa.area_conocimiento),
                joinedload(Programa.car_innovacion)
            )
        )
        result = self.db.execute(stmt)
        return result.scalars().first()

    async def guardar(self, entidad: Programa, esquema: str = None):
        try:
            self.db.add(entidad)
            self.db.commit()
            self.db.refresh(entidad)
            return True, "Programa guardado correctamente"
        except Exception as e:
            self.db.rollback()
            return False, f"Error al guardar: {str(e)}"

    async def actualizar(self, valor_id: int, datos: dict, esquema: str = None):
        """
        Actualización directa y eficiente usando SQLAlchemy 2.0 style.
        """
        try:
            stmt = (
                update(Programa)
                .where(Programa.id == valor_id)
                .values(**datos)
            )
            result = self.db.execute(stmt)
            self.db.commit()
            
            if result.rowcount > 0:
                return True, "Programa actualizado con éxito"
            return False, "No se encontró el programa para actualizar"
        except Exception as e:
            self.db.rollback()
            return False, f"Error al actualizar: {str(e)}"

    async def eliminar(self, entidad: Programa, esquema: str = None):
        try:
            self.db.delete(entidad)
            self.db.commit()
            return True, "Programa eliminado correctamente"
        except Exception as e:
            self.db.rollback()
            return False, f"Error al eliminar: {str(e)}"