from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from .abstracciones.i_repository import IRepository
from models.aa_rc import AaRc 

class AaRcRepository(IRepository):

    def __init__(self, db: AsyncSession): # Cambiado a AsyncSession
        self.db = db

    async def obtener_todos(self, esquema: str = None, limite: int = None):
        stmt = select(AaRc)
        if limite:
            stmt = stmt.limit(limite)
        
        # CORRECCIÓN: await para ejecutar la consulta
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def obtener_por_id(self, valor_id, esquema: str = None):
        return None 

    async def obtener_por_llave_compuesta(self, id_curso: int, cod_reg: int, esquema: str = None):
        stmt = select(AaRc).where(
            AaRc.id_curso == id_curso,
            AaRc.codigo_registro == cod_reg
        )
        # CORRECCIÓN: await para ejecutar
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def guardar(self, entidad: AaRc, esquema: str = None):
        try:
            self.db.add(entidad)
            # CORRECCIÓN: await en commit y refresh
            await self.db.commit()
            await self.db.refresh(entidad)
            return True, "Registro guardado correctamente"
        except Exception as e:
            await self.db.rollback() # CORRECCIÓN: await en rollback
            return False, f"Error: {str(e)}"

    async def actualizar(self, id_curso: int, cod_reg: int, datos: dict, esquema: str = None):
        try:
            stmt = update(AaRc).where(
                AaRc.id_curso == id_curso,
                AaRc.codigo_registro == cod_reg
            ).values(**datos)
            
            # CORRECCIÓN: await en execute y commit
            result = await self.db.execute(stmt)
            await self.db.commit()
            
            if result.rowcount > 0:
                return True, "Registro actualizado correctamente"
            return False, "No se encontró el registro para actualizar"
        except Exception as e:
            await self.db.rollback()
            return False, f"Error al actualizar: {str(e)}"

    async def eliminar(self, entidad: AaRc, esquema: str = None):
        try:
            # CORRECCIÓN: await en delete y commit
            await self.db.delete(entidad)
            await self.db.commit()
            return True, "Registro eliminado correctamente"
        except Exception as e:
            await self.db.rollback()
            return False, f"Error: {str(e)}"