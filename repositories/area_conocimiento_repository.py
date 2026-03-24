from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from .abstracciones.i_repository import IRepository
from models.area_conocimiento import AreaConocimiento

class AreaConocimientoRepository(IRepository):

    def __init__(self, db: AsyncSession): # Cambiado a AsyncSession
        self.db = db

    async def obtener_todos(self, esquema: str = None, limite: int = None):
        stmt = select(AreaConocimiento)
        if limite:
            stmt = stmt.limit(limite)
        
        # CORRECCIÓN: await para ejecutar
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def obtener_por_id(self, valor_id: int, esquema: str = None):
        stmt = select(AreaConocimiento).where(AreaConocimiento.id == valor_id)
        # CORRECCIÓN: await para ejecutar
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def guardar(self, entidad: AreaConocimiento, esquema: str = None):
        try:
            self.db.add(entidad)
            # CORRECCIÓN: await en commit y refresh
            await self.db.commit()
            await self.db.refresh(entidad)
            return True, "Área de conocimiento guardada correctamente"
        except Exception as e:
            # CORRECCIÓN: await en rollback
            await self.db.rollback()
            return False, f"Error: {str(e)}"

    async def actualizar(self, valor_id: int, datos: dict, esquema: str = None):
        try:
            stmt = (
                update(AreaConocimiento)
                .where(AreaConocimiento.id == valor_id)
                .values(**datos)
            )
            
            # CORRECCIÓN: await en execute y commit
            result = await self.db.execute(stmt)
            await self.db.commit()
            
            if result.rowcount > 0:
                return True, "Área de conocimiento actualizada con éxito"
            return False, "No se encontró el registro para actualizar"
        except Exception as e:
            # CORRECCIÓN: await en rollback
            await self.db.rollback()
            return False, f"Error al actualizar: {str(e)}"

    async def eliminar(self, entidad: AreaConocimiento, esquema: str = None):
        try:
            # CORRECCIÓN: await en delete y commit
            await self.db.delete(entidad)
            await self.db.commit()
            return True, "Registro eliminado correctamente"
        except Exception as e:
            # CORRECCIÓN: await en rollback
            await self.db.rollback()
            return False, f"Error: {str(e)}"