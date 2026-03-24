from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select, update
from .abstracciones.i_repository import IRepository
from models.rol import Rol

class RolRepository(IRepository):

    def __init__(self, db: AsyncSession): # Inyectamos la sesión asíncrona
        self.db = db

    async def obtener_todos(self, esquema: str = None, limite: int = None):
        """Lista todos los roles disponibles en el sistema."""
        stmt = select(Rol)
        if limite:
            stmt = stmt.limit(limite)
        
        # CORRECCIÓN: await para ejecución asíncrona
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def obtener_por_id(self, valor_id: int, esquema: str = None):
        """Obtiene un rol específico y sus usuarios asociados."""
        # CORRECCIÓN: selectinload es más seguro para colecciones en async
        stmt = select(Rol).where(Rol.id == valor_id).options(
            selectinload(Rol.usuario)
        )
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def guardar(self, entidad: Rol, esquema: str = None):
        try:
            self.db.add(entidad)
            # CORRECCIÓN: await en operaciones de escritura
            await self.db.commit()
            await self.db.refresh(entidad)
            return True, "Rol guardado correctamente"
        except Exception as e:
            # CORRECCIÓN: await en rollback
            await self.db.rollback()
            return False, f"Error: {str(e)}"

    async def actualizar(self, valor_id: int, datos: dict, esquema: str = None):
        """
        Actualiza los datos de un rol.
        """
        try:
            stmt = (
                update(Rol)
                .where(Rol.id == valor_id)
                .values(**datos)
            )
            # CORRECCIÓN: await en execute y commit
            result = await self.db.execute(stmt)
            await self.db.commit()
            
            if result.rowcount > 0:
                return True, "Rol actualizado correctamente"
            return False, "No se encontró el rol para actualizar"
        except Exception as e:
            await self.db.rollback()
            return False, f"Error al actualizar: {str(e)}"

    async def eliminar(self, entidad: Rol, esquema: str = None):
        try:
            # CORRECCIÓN: await en delete y commit
            await self.db.delete(entidad)
            await self.db.commit()
            return True, "Rol eliminado correctamente"
        except Exception as e:
            await self.db.rollback()
            return False, f"Error: {str(e)}"

    async def obtener_por_nombre(self, nombre: str):
        """Útil para validaciones de seguridad o inyección de roles iniciales."""
        stmt = select(Rol).where(Rol.nombre == nombre)
        # CORRECCIÓN: await para ejecución
        result = await self.db.execute(stmt)
        return result.scalars().first()