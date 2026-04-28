from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from .abstracciones.i_repository import IRepository
from models.asociaciones import Asociaciones 

class AsociacionesRepository(IRepository):

    def __init__(self, db: AsyncSession):
        self.db = db

    async def obtener_todos(self, esquema: str = None, limite: int = None):
        stmt = select(Asociaciones)
        if limite:
            stmt = stmt.limit(limite)
        
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def obtener_por_id(self, valor_id: int, esquema: str = None):
        stmt = select(Asociaciones).where(Asociaciones.id == valor_id)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def guardar(self, entidad: Asociaciones, esquema: str = None):
        try:
            self.db.add(entidad)
            await self.db.commit()
            await self.db.refresh(entidad)
            return True, "Asociación guardada correctamente"
        except Exception as e:
            await self.db.rollback()
            return False, f"Error al guardar: {str(e)}"

    async def actualizar(self, valor_id: int, datos: dict, esquema: str = None):
        try:
            stmt = (
                update(Asociaciones)
                .where(Asociaciones.id == valor_id)
                .values(**datos)
            )
            
            result = await self.db.execute(stmt)
            await self.db.commit()
            
            if result.rowcount > 0:
                return True, "Asociación actualizada correctamente"
            return False, "No se encontró la asociación para actualizar"
        except Exception as e:
            await self.db.rollback()
            return False, f"Error al actualizar: {str(e)}"

    async def eliminar(self, entidad: Asociaciones, esquema: str = None):
        try:
            await self.db.delete(entidad)
            await self.db.commit()
            return True, "Asociación eliminada correctamente"
        except Exception as e:
            await self.db.rollback()
            return False, f"Error al eliminar: {str(e)}"