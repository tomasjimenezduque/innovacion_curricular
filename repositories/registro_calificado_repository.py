from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy import select, update
from .abstracciones.i_repository import IRepository
from models.registro_calificado import RegistroCalificado

class RegistroCalificadoRepository(IRepository):

    def __init__(self, db: AsyncSession): # Inyectamos la sesión asíncrona
        self.db = db

    async def obtener_todos(self, esquema: str = None, limite: int = None):
        """Lista los registros cargando el programa asociado para evitar N+1."""
        stmt = select(RegistroCalificado).options(joinedload(RegistroCalificado.programa_))
        if limite:
            stmt = stmt.limit(limite)
        
        # CORRECCIÓN: await para ejecución asíncrona
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def obtener_por_id(self, valor_id: int, esquema: str = None):
        """Busca por el campo 'codigo' y carga enfoques y actividades."""
        stmt = (
            select(RegistroCalificado)
            .where(RegistroCalificado.codigo == valor_id)
            .options(
                # joinedload es ideal para relaciones 1:1 (como el programa si fuera el caso)
                # selectinload es mejor para colecciones (listas) en modo asíncrono
                selectinload(RegistroCalificado.enfoque),
                selectinload(RegistroCalificado.aa_rc)
            )
        )
        # CORRECCIÓN: await para ejecución
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def guardar(self, entidad: RegistroCalificado, esquema: str = None):
        try:
            self.db.add(entidad)
            # CORRECCIÓN: await en operaciones de escritura
            await self.db.commit()
            await self.db.refresh(entidad)
            return True, "Registro Calificado guardado correctamente"
        except Exception as e:
            # CORRECCIÓN: await en rollback
            await self.db.rollback()
            return False, f"Error: {str(e)}"

    async def actualizar(self, codigo: int, datos: dict, esquema: str = None):
        """
        Actualización directa por código usando el estándar de SQLAlchemy 2.0.
        """
        try:
            stmt = (
                update(RegistroCalificado)
                .where(RegistroCalificado.codigo == codigo)
                .values(**datos)
            )
            # CORRECCIÓN: await en execute y commit
            result = await self.db.execute(stmt)
            await self.db.commit()
            
            if result.rowcount > 0:
                return True, "Registro Calificado actualizado correctamente"
            return False, "No se encontró el registro para actualizar"
        except Exception as e:
            await self.db.rollback()
            return False, f"Error al actualizar: {str(e)}"

    async def eliminar(self, entidad: RegistroCalificado, esquema: str = None):
        try:
            # CORRECCIÓN: await en delete y commit
            await self.db.delete(entidad)
            await self.db.commit()
            return True, "Registro Calificado eliminado"
        except Exception as e:
            await self.db.rollback()
            return False, f"Error: {str(e)}"