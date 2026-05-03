from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from .abstracciones.i_repository import IRepository
from models.aliado import Aliado

class AliadoRepository(IRepository):

    def __init__(self, db: AsyncSession):
        """Constructor que recibe la sesión asíncrona de la base de datos."""
        self.db = db

    async def obtener_todos(self, esquema: str = None, limite: int = None):
        """Obtiene la lista de todos los aliados de forma eficiente."""
        try:
            stmt = select(Aliado)
            if limite:
                stmt = stmt.limit(limite)
            
            result = await self.db.execute(stmt)
            # .unique() asegura que no haya duplicados si luego usas joins
            # .all() consume el resultado para que la sesión pueda cerrarse limpia
            return result.scalars().unique().all()
        except Exception as e:
            print(f"❌ Error en obtener_todos: {e}")
            return []

    async def obtener_por_id(self, valor_id: str, esquema: str = None):
        """Busca un aliado por su NIT."""
        try:
            stmt = select(Aliado).where(Aliado.nit == str(valor_id))
            result = await self.db.execute(stmt)
            return result.scalars().first()
        except Exception as e:
            print(f"❌ Error en obtener_por_id: {e}")
            return None

    async def guardar(self, entidad: Aliado, esquema: str = None):
        """Guarda un nuevo aliado con gestión de commit explícito."""
        try:
            self.db.add(entidad)
            await self.db.commit()
            await self.db.refresh(entidad)
            return True, "Aliado guardado correctamente"
        except Exception as e:
            await self.db.rollback()
            return False, f"Error al guardar: {str(e)}"

    async def actualizar(self, valor_id: str, datos: dict, esquema: str = None):
        """Actualiza un aliado usando update() para evitar cargas innecesarias."""
        try:
            stmt = (
                update(Aliado)
                .where(Aliado.nit == str(valor_id))
                .values(**datos)
                .execution_options(synchronize_session="fetch")
            )
            
            result = await self.db.execute(stmt)
            await self.db.commit()
            
            if result.rowcount > 0:
                return True, "Aliado actualizado correctamente"
            return False, "No se encontró el aliado con ese NIT"
        except Exception as e:
            await self.db.rollback()
            return False, f"Error al actualizar: {str(e)}"

    async def eliminar(self, entidad: Aliado, esquema: str = None):
        """Elimina el registro y confirma la transacción."""
        try:
            await self.db.delete(entidad)
            await self.db.commit()
            return True, "Registro eliminado correctamente"
        except Exception as e:
            await self.db.rollback()
            return False, f"Error al eliminar: {str(e)}"