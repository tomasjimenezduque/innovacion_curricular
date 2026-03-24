from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy import select, update
from .abstracciones.i_repository import IRepository
from models.programa import Programa

class ProgramaRepository(IRepository):

    def __init__(self, db: AsyncSession): # Inyectamos AsyncSession
        self.db = db

    async def obtener_todos(self, esquema: str = None, limite: int = None):
        """
        Obtiene todos los programas cargando la facultad para optimizar.
        """
        # CORRECCIÓN: Usamos await para la ejecución asíncrona
        stmt = select(Programa).options(joinedload(Programa.facultad_))
        if limite:
            stmt = stmt.limit(limite)
        
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def obtener_por_id(self, valor_id: int, esquema: str = None):
        """
        Carga el programa con sus relaciones Many-to-Many.
        Nota: Para colecciones (listas), a veces es más eficiente usar selectinload.
        """
        stmt = (
            select(Programa)
            .where(Programa.id == valor_id)
            .options(
                joinedload(Programa.facultad_),
                # Para relaciones Many-to-Many o colecciones grandes, 
                # selectinload suele ser más performante que joinedload.
                selectinload(Programa.area_conocimiento),
                selectinload(Programa.car_innovacion)
            )
        )
        # CORRECCIÓN: await para la ejecución
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def guardar(self, entidad: Programa, esquema: str = None):
        try:
            self.db.add(entidad)
            # CORRECCIÓN: await en commit y refresh
            await self.db.commit()
            await self.db.refresh(entidad)
            return True, "Programa guardado correctamente"
        except Exception as e:
            # CORRECCIÓN: await en rollback
            await self.db.rollback()
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
            # CORRECCIÓN: await en execute y commit
            result = await self.db.execute(stmt)
            await self.db.commit()
            
            if result.rowcount > 0:
                return True, "Programa actualizado con éxito"
            return False, "No se encontró el programa para actualizar"
        except Exception as e:
            # CORRECCIÓN: await en rollback
            await self.db.rollback()
            return False, f"Error al actualizar: {str(e)}"

    async def eliminar(self, entidad: Programa, esquema: str = None):
        try:
            # CORRECCIÓN: await en delete y commit
            await self.db.delete(entidad)
            await self.db.commit()
            return True, "Programa eliminado correctamente"
        except Exception as e:
            # CORRECCIÓN: await en rollback
            await self.db.rollback()
            return False, f"Error al eliminar: {str(e)}"