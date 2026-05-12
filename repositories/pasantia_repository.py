from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, text, func
from .abstracciones.i_repository import IRepository
from models.pasantia import Pasantia

class PasantiaRepository(IRepository):

    def __init__(self, db: AsyncSession):
        self.db = db

    async def obtener_todos(self, esquema: str = None, limite: int = None):
        stmt = select(Pasantia)
        if limite:
            stmt = stmt.limit(limite)
        result = await self.db.execute(stmt)
        filas = result.scalars().all()
        resultado_limpio = []
        for f in filas:
            d = f.__dict__.copy()
            d.pop('_sa_instance_state', None)
            resultado_limpio.append(d)
        return resultado_limpio

    async def obtener_por_id(self, valor_id: int, esquema: str = None):
        stmt = select(Pasantia).where(Pasantia.id == valor_id)
        result = await self.db.execute(stmt)
        fila = result.scalars().first()
        return fila.__dict__ if fila else None

    async def guardar(self, datos: dict, esquema: str = None):
        try:
            datos.pop('id', None)
            resultado = await self.db.execute(select(func.max(Pasantia.id)))
            max_id = resultado.scalar() or 0
            datos['id'] = max_id + 1

            entidad = Pasantia(**datos)
            self.db.add(entidad)
            await self.db.commit()
            return True, "Pasantía guardada correctamente"
        except Exception as e:
            await self.db.rollback()
            print(f"ERROR REPO PASANTIA (GUARDAR): {e}")
            return False, f"Error: {str(e)}"

    async def actualizar(self, valor_id: int, datos: dict, esquema: str = None):
        try:
            datos.pop('id', None)
            stmt = update(Pasantia).where(Pasantia.id == valor_id).values(**datos)
            result = await self.db.execute(stmt)
            await self.db.commit()
            if result.rowcount > 0:
                return True, "Pasantía actualizada correctamente"
            return False, "No se encontró la pasantía"
        except Exception as e:
            await self.db.rollback()
            return False, f"Error al actualizar: {str(e)}"

    async def eliminar(self, entidad: dict, esquema: str = None):
        try:
            valor_id = entidad.get('id') if isinstance(entidad, dict) else entidad.id
            sql = text("DELETE FROM pasantia WHERE id = :id_val")
            await self.db.execute(sql, {"id_val": valor_id})
            await self.db.commit()
            return True, "Pasantía eliminada correctamente"
        except Exception as e:
            await self.db.rollback()
            return False, f"Error: {str(e)}"