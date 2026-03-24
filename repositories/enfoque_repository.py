from sqlalchemy.ext.asyncio import AsyncSession # Cambio clave
from sqlalchemy import select, update
from .abstracciones.i_repository import IRepository
from models.enfoque import Enfoque

class EnfoqueRepository(IRepository):

    def __init__(self, db: AsyncSession): # Ahora recibe AsyncSession
        self.db = db

    async def obtener_todos(self, esquema: str = None, limite: int = None):
        stmt = select(Enfoque)
        if limite:
            stmt = stmt.limit(limite)
        
        # CORRECCIÓN: await para esperar la respuesta de la DB
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def obtener_por_id(self, valor_id: int, esquema: str = None):
        stmt = select(Enfoque).where(Enfoque.id == valor_id)
        # CORRECCIÓN: await para ejecutar la consulta
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def guardar(self, entidad: Enfoque, esquema: str = None):
        try:
            self.db.add(entidad)
            # CORRECCIÓN: await en operaciones de escritura
            await self.db.commit()
            await self.db.refresh(entidad)
            return True, "Enfoque guardado correctamente"
        except Exception as e:
            # CORRECCIÓN: rollback también debe ser esperado
            await self.db.rollback()
            return False, f"Error: {str(e)}"

    async def actualizar(self, valor_id: int, datos: dict, esquema: str = None):
        try:
            stmt = (
                update(Enfoque)
                .where(Enfoque.id == valor_id)
                .values(**datos)
            )
            
            # CORRECCIÓN: await en execute y commit
            result = await self.db.execute(stmt)
            await self.db.commit()
            
            if result.rowcount > 0:
                return True, "Enfoque actualizado correctamente"
            return False, "No se encontró el enfoque para actualizar"
        except Exception as e:
            await self.db.rollback()
            return False, f"Error al actualizar el enfoque: {str(e)}"

    async def eliminar(self, entidad: Enfoque, esquema: str = None):
        try:
            # CORRECCIÓN: await en delete y commit
            await self.db.delete(entidad)
            await self.db.commit()
            return True, "Registro eliminado correctamente"
        except Exception as e:
            await self.db.rollback()
            return False, f"Error: {str(e)}"