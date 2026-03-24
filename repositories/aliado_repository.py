from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from .abstracciones.i_repository import IRepository
from models.aliado import Aliado

class AliadoRepository(IRepository):

    def __init__(self, db: AsyncSession): # Cambiado a AsyncSession
        self.db = db

    async def obtener_todos(self, esquema: str = None, limite: int = None):
        stmt = select(Aliado)
        if limite:
            stmt = stmt.limit(limite)
        
        # CORRECCIÓN: await para ejecutar
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def obtener_por_id(self, valor_id: int, esquema: str = None):
        stmt = select(Aliado).where(Aliado.id == valor_id)
        # CORRECCIÓN: await para ejecutar
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def guardar(self, entidad: Aliado, esquema: str = None):
        try:
            self.db.add(entidad)
            # CORRECCIÓN: await en commit y refresh
            await self.db.commit()
            await self.db.refresh(entidad)
            return True, "Aliado guardado correctamente"
        except Exception as e:
            # CORRECCIÓN: await en rollback
            await self.db.rollback()
            return False, f"Error: {str(e)}"

    async def actualizar(self, valor_id: int, datos: dict, esquema: str = None):
        try:
            stmt = (
                update(Aliado)
                .where(Aliado.id == valor_id)
                .values(**datos)
            )
            
            # CORRECCIÓN: await en execute y commit
            result = await self.db.execute(stmt)
            await self.db.commit()
            
            if result.rowcount > 0:
                return True, "Aliado actualizado correctamente"
            return False, "No se encontró el aliado para actualizar"
        except Exception as e:
            # CORRECCIÓN: await en rollback
            await self.db.rollback()
            return False, f"Error al actualizar aliado: {str(e)}"

    async def eliminar(self, entidad: Aliado, esquema: str = None):
        try:
            # CORRECCIÓN: await en delete y commit
            await self.db.delete(entidad)
            await self.db.commit()
            return True, "Registro eliminado correctamente"
        except Exception as e:
            # CORRECCIÓN: await en rollback
            await self.db.rollback()
            return False, f"Error: {str(e)}"