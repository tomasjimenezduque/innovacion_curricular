from sqlalchemy.ext.asyncio import AsyncSession # Cambio a AsyncSession
from sqlalchemy import select, update
from .abstracciones.i_repository import IRepository
from models.premio import Premio

class PremioRepository(IRepository):

    def __init__(self, db: AsyncSession): # Ahora inyectamos AsyncSession
        self.db = db

    async def obtener_todos(self, esquema: str = None, limite: int = None):
        """Consulta asíncrona de todas las facultades."""
        stmt = select(Premio)
        if limite:
            stmt = stmt.limit(limite)
        
        # CORRECCIÓN: await para ejecutar
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def obtener_por_id(self, valor_id: int, esquema: str = None):
        """Obtiene una facultad específica por su ID."""
        stmt = select(Premio).where(Premio.id == valor_id)
        # CORRECCIÓN: await para ejecutar
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def guardar(self, entidad: Premio, esquema: str = None):
        try:
            self.db.add(entidad)
            # CORRECCIÓN: await en commit y refresh
            await self.db.commit()
            await self.db.refresh(entidad)
            return True, "Premio guardado correctamente"
        except Exception as e:
            # CORRECCIÓN: await en rollback
            await self.db.rollback()
            return False, f"Error: {str(e)}"

    async def actualizar(self, valor_id: int, datos: dict, esquema: str = None):
        """
        Actualiza los datos de un premio (nombre, fecha, institución, etc.).
        """
        try:
            stmt = (
                update(Premio)
                .where(Premio.id == valor_id)
                .values(**datos)
            )
            
            # CORRECCIÓN: await en execute y commit
            result = await self.db.execute(stmt)
            await self.db.commit()
            
            if result.rowcount > 0:
                return True, "Premio actualizado correctamente"
            return False, "No se encontró el premio para actualizar"
        except Exception as e:
            await self.db.rollback()
            return False, f"Error al actualizar premio: {str(e)}"

    async def eliminar(self, entidad: Premio, esquema: str = None):
        try:
            # CORRECCIÓN: await en delete y commit
            await self.db.delete(entidad)
            await self.db.commit()
            return True, "Registro eliminado correctamente"
        except Exception as e:
            await self.db.rollback()
            return False, f"Error: {str(e)}"