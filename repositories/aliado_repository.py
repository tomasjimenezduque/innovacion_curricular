from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from .abstracciones.i_repository import IRepository
from models.aliado import Aliado

class AliadoRepository(IRepository):

    def __init__(self, db: AsyncSession):
        """Constructor que recibe la sesión asíncrona de la base de datos."""
        self.db = db

    async def obtener_todos(self, esquema: str = None, limite: int = None):
        """Obtiene la lista de todos los aliados."""
        stmt = select(Aliado)
        if limite:
            stmt = stmt.limit(limite)
        
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def obtener_por_id(self, valor_id: str, esquema: str = None):
        """
        Busca un aliado por su NIT (que ahora actúa como ID).
        Nota: valor_id ahora es str.
        """
        stmt = select(Aliado).where(Aliado.nit == valor_id)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def guardar(self, entidad: Aliado, esquema: str = None):
        """Guarda un nuevo aliado en la base de datos."""
        try:
            self.db.add(entidad)
            await self.db.commit()
            await self.db.refresh(entidad)
            return True, "Aliado guardado correctamente"
        except Exception as e:
            await self.db.rollback()
            return False, f"Error al guardar: {str(e)}"

    async def actualizar(self, valor_id: str, datos: dict, esquema: str = None):
        """
        Actualiza un aliado existente usando el NIT como referencia.
        """
        try:
            stmt = (
                update(Aliado)
                .where(Aliado.nit == valor_id)
                .values(**datos)
            )
            
            result = await self.db.execute(stmt)
            await self.db.commit()
            
            if result.rowcount > 0:
                return True, "Aliado actualizado correctamente"
            return False, "No se encontró el aliado con ese NIT para actualizar"
        except Exception as e:
            await self.db.rollback()
            return False, f"Error al actualizar aliado: {str(e)}"

    async def eliminar(self, entidad: Aliado, esquema: str = None):
        """Elimina un objeto aliado de la base de datos."""
        try:
            await self.db.delete(entidad)
            await self.db.commit()
            return True, "Registro eliminado correctamente"
        except Exception as e:
            await self.db.rollback()
            return False, f"Error al eliminar: {str(e)}"