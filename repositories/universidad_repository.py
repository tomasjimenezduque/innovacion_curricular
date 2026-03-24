from sqlalchemy.ext.asyncio import AsyncSession # Cambio a sesión asíncrona
from sqlalchemy.orm import selectinload
from sqlalchemy import select, update
from .abstracciones.i_repository import IRepository
from models.universidad import Universidad

class UniversidadRepository(IRepository):

    def __init__(self, db: AsyncSession): # Inyectamos AsyncSession
        self.db = db

    async def obtener_todos(self, esquema: str = None, limite: int = None):
        """Lista todas las universidades registradas."""
        stmt = select(Universidad)
        if limite:
            stmt = stmt.limit(limite)
        
        # CORRECCIÓN: await para ejecución asíncrona
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def obtener_por_id(self, valor_id: int, esquema: str = None):
        """
        Obtiene una universidad y sus facultades asociadas.
        """
        # CORRECCIÓN: Usamos selectinload para cargar la colección de facultades
        stmt = select(Universidad).where(Universidad.id == valor_id).options(
            selectinload(Universidad.facultad)
        )
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def guardar(self, entidad: Universidad, esquema: str = None):
        try:
            self.db.add(entidad)
            # CORRECCIÓN: await en operaciones de escritura
            await self.db.commit()
            await self.db.refresh(entidad)
            return True, "Universidad guardada correctamente"
        except Exception as e:
            # CORRECCIÓN: await en rollback
            await self.db.rollback()
            return False, f"Error: {str(e)}"

    async def actualizar(self, valor_id: int, datos: dict, esquema: str = None):
        """
        Actualiza los datos de la institución.
        """
        try:
            stmt = (
                update(Universidad)
                .where(Universidad.id == valor_id)
                .values(**datos)
            )
            # CORRECCIÓN: await en execute y commit
            result = await self.db.execute(stmt)
            await self.db.commit()
            
            if result.rowcount > 0:
                return True, "Universidad actualizada con éxito"
            return False, "No se encontró la universidad para actualizar"
        except Exception as e:
            await self.db.rollback()
            return False, f"Error al actualizar: {str(e)}"

    async def eliminar(self, entidad: Universidad, esquema: str = None):
        try:
            # CORRECCIÓN: await en delete y commit
            await self.db.delete(entidad)
            await self.db.commit()
            return True, "Universidad eliminada correctamente"
        except Exception as e:
            await self.db.rollback()
            return False, f"Error: {str(e)}"