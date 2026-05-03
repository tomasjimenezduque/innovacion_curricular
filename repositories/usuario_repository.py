from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy import select, update, insert
from .abstracciones.i_repository import IRepository
from models.usuario import Usuario

class UsuarioRepository(IRepository):

    def __init__(self, db: AsyncSession):
        self.db = db

    async def obtener_todos(self, esquema: str = None, limite: int = None):
        """Lista usuarios de forma eficiente."""
        stmt = select(Usuario)
        if limite:
            stmt = stmt.limit(limite)
        
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def obtener_por_id(self, valor_id: int, esquema: str = None):
        """Obtiene un usuario detallado con sus roles asignados."""
        stmt = select(Usuario).where(Usuario.id == valor_id).options(
            joinedload(Usuario.rol)
        )
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def guardar(self, datos: dict, esquema: str = None):
        """
        Opción B: Inserta un usuario directamente desde un diccionario.
        """
        try:
            # Usamos la expresión insert() para mayor eficiencia con diccionarios
            stmt = insert(Usuario).values(**datos)
            await self.db.execute(stmt)
            await self.db.commit()
            return True, "Usuario creado exitosamente"
        except Exception as e:
            await self.db.rollback()
            return False, f"Error al crear usuario: {str(e)}"

    async def actualizar(self, valor_id: int, datos: dict, esquema: str = None):
        """Actualiza los datos del usuario."""
        try:
            stmt = (
                update(Usuario)
                .where(Usuario.id == valor_id)
                .values(**datos)
            )
            result = await self.db.execute(stmt)
            await self.db.commit()
            
            if result.rowcount > 0:
                return True, "Usuario actualizado con éxito"
            return False, "No se encontró el usuario para actualizar"
        except Exception as e:
            await self.db.rollback()
            return False, f"Error al actualizar: {str(e)}"

    async def eliminar(self, entidad: Usuario, esquema: str = None):
        try:
            await self.db.delete(entidad)
            await self.db.commit()
            return True, "Usuario eliminado correctamente"
        except Exception as e:
            await self.db.rollback()
            return False, f"Error: {str(e)}"

    async def obtener_por_username(self, username: str):
        """Método clave para el flujo de autenticación."""
        stmt = select(Usuario).where(Usuario.username == username).options(
            joinedload(Usuario.rol)
        )
        result = await self.db.execute(stmt)
        return result.scalars().first()