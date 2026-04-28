from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, delete
# Importamos las tablas definidas en tu modelo
from models.asociaciones import (
    t_rol_usuario, 
    t_programa_ac, 
    t_an_programa, 
    t_programa_ci, 
    t_programa_pe, 
    t_enfoque_rc
)

class AsociacionesRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    # --- Gestión de Rol y Usuario ---
    async def asociar_rol_usuario(self, usuario_id: int, rol_id: int):
        try:
            stmt = insert(t_rol_usuario).values(usuario_id=usuario_id, rol_id=rol_id)
            await self.db.execute(stmt)
            await self.db.commit()
            return True, "Rol asignado al usuario correctamente"
        except Exception as e:
            await self.db.rollback()
            return False, f"Error: {str(e)}"

    # --- Gestión de Programa y Área de Conocimiento ---
    async def asociar_programa_area(self, programa_id: int, area_id: int):
        try:
            stmt = insert(t_programa_ac).values(programa=programa_id, area_conocimiento=area_id)
            await self.db.execute(stmt)
            await self.db.commit()
            return True, "Área vinculada al programa"
        except Exception as e:
            await self.db.rollback()
            return False, f"Error: {str(e)}"

    # --- Gestión de Aspecto Normativo y Programa ---
    async def asociar_an_programa(self, an_id: int, programa_id: int):
        try:
            stmt = insert(t_an_programa).values(aspecto_normativo=an_id, programa=programa_id)
            await self.db.execute(stmt)
            await self.db.commit()
            return True, "Aspecto normativo vinculado"
        except Exception as e:
            await self.db.rollback()
            return False, f"Error: {str(e)}"

    # --- Método Genérico para Desvincular (Borrar de tabla intermedia) ---
    async def eliminar_asociacion(self, tabla, filtros: dict):
        """
        Ejemplo de uso: eliminar_asociacion(t_rol_usuario, {"usuario_id": 1, "rol_id": 2})
        """
        try:
            stmt = delete(tabla).filter_by(**filtros)
            await self.db.execute(stmt)
            await self.db.commit()
            return True, "Desvinculación exitosa"
        except Exception as e:
            await self.db.rollback()
            return False, f"Error al desvincular: {str(e)}"

    # --- Obtener todos (Ejemplo para una tabla específica) ---
    async def obtener_roles_por_usuario(self, usuario_id: int):
        stmt = select(t_rol_usuario).where(t_rol_usuario.c.usuario_id == usuario_id)
        result = await self.db.execute(stmt)
        return result.fetchall()
    
    async def asociar_generico(self, tabla, datos: dict):
        try:
            from sqlalchemy import insert
            stmt = insert(tabla).values(**datos)
            await self.db.execute(stmt)
            await self.db.commit()
            return True, "Asociación creada"
        except Exception as e:
            await self.db.rollback()
            return False, str(e)