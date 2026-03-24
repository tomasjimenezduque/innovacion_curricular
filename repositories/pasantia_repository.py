from sqlalchemy.ext.asyncio import AsyncSession # Cambio a AsyncSession
from sqlalchemy import select, update
from .abstracciones.i_repository import IRepository
from models.pasantia import Pasantia

class PasantiaRepository(IRepository):

    def __init__(self, db: AsyncSession): # Recibe AsyncSession
        self.db = db

    async def obtener_todos(self, esquema: str = None, limite: int = None):
        """Consulta asíncrona de todas las pasantías registradas."""
        stmt = select(Pasantia)
        if limite:
            stmt = stmt.limit(limite)
        
        # CORRECCIÓN: await para ejecutar la consulta
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def obtener_por_id(self, valor_id: int, esquema: str = None):
        """Obtiene una pasantía específica por su identificador único."""
        stmt = select(Pasantia).where(Pasantia.id == valor_id)
        # CORRECCIÓN: await para ejecutar la consulta
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def guardar(self, entidad: Pasantia, esquema: str = None):
        try:
            self.db.add(entidad)
            # CORRECCIÓN: await en commit y refresh
            await self.db.commit()
            await self.db.refresh(entidad)
            return True, "Pasantía guardada correctamente"
        except Exception as e:
            # CORRECCIÓN: await en rollback
            await self.db.rollback()
            return False, f"Error: {str(e)}"

    async def actualizar(self, valor_id: int, datos: dict, esquema: str = None):
        """
        Actualiza los datos de una pasantía (empresa, tutor, fechas, etc.).
        """
        try:
            stmt = (
                update(Pasantia)
                .where(Pasantia.id == valor_id)
                .values(**datos)
            )
            
            # CORRECCIÓN: await en execute y commit
            result = await self.db.execute(stmt)
            await self.db.commit()
            
            if result.rowcount > 0:
                return True, "Pasantía actualizada correctamente"
            return False, "No se encontró la pasantía para actualizar"
        except Exception as e:
            await self.db.rollback()
            return False, f"Error al actualizar pasantía: {str(e)}"

    async def eliminar(self, entidad: Pasantia, esquema: str = None):
        try:
            # CORRECCIÓN: await en delete y commit
            await self.db.delete(entidad)
            await self.db.commit()
            return True, "Registro eliminado correctamente"
        except Exception as e:
            await self.db.rollback()
            return False, f"Error: {str(e)}"