from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select, update, text
from .abstracciones.i_repository import IRepository
from models.rol import Rol

class RolRepository(IRepository):

    def __init__(self, db: AsyncSession):
        self.db = db

    async def obtener_todos(self, esquema: str = None, limite: int = None):
        stmt = select(Rol)
        if limite:
            stmt = stmt.limit(limite)
        
        result = await self.db.execute(stmt)
        # Convertimos a diccionario para que el Frontend lo entienda fácil
        return [r.__dict__ for r in result.scalars().all()]

    async def obtener_por_id(self, valor_id: int, esquema: str = None):
        stmt = select(Rol).where(Rol.id == valor_id)
        result = await self.db.execute(stmt)
        fila = result.scalars().first()
        return fila.__dict__ if fila else None

    async def guardar(self, datos: dict, esquema: str = None):
        """
        FIX: Ahora acepta un diccionario y lo convierte a objeto Rol.
        Esto elimina el Error 500 que viste en los logs.
        """
        try:
            # Convertimos el diccionario en una instancia del Modelo
            nueva_entidad = Rol(**datos)
            self.db.add(nueva_entidad)
            await self.db.commit()
            await self.db.refresh(nueva_entidad)
            return True, "Rol guardado correctamente"
        except Exception as e:
            await self.db.rollback()
            print(f"ERROR REPO ROL (GUARDAR): {e}")
            return False, f"Error: {str(e)}"

    async def actualizar(self, valor_id: int, datos: dict, esquema: str = None):
        try:
            # Aseguramos que no se intente actualizar el ID
            if "id" in datos: datos.pop("id")
            
            stmt = (
                update(Rol)
                .where(Rol.id == valor_id)
                .values(**datos)
            )
            result = await self.db.execute(stmt)
            await self.db.commit()
            
            if result.rowcount > 0:
                return True, "Rol actualizado correctamente"
            return False, "No se encontró el rol"
        except Exception as e:
            await self.db.rollback()
            return False, f"Error: {str(e)}"

    async def eliminar(self, valor_id: int, esquema: str = None):
        """
        LECCIÓN APRENDIDA: Usamos text() para evitar errores de expresión SQL.
        """
        try:
            # Se puede recibir el ID directamente o la entidad. Aquí lo hacemos por ID:
            sql = text("DELETE FROM rol WHERE id = :id_val")
            await self.db.execute(sql, {"id_val": valor_id})
            await self.db.commit()
            return True, "Rol eliminado correctamente"
        except Exception as e:
            await self.db.rollback()
            print(f"ERROR REPO ROL (ELIMINAR): {e}")
            return False, f"Error: {str(e)}"

    async def obtener_por_nombre(self, nombre: str):
        stmt = select(Rol).where(Rol.nombre == nombre)
        result = await self.db.execute(stmt)
        fila = result.scalars().first()
        return fila.__dict__ if fila else None