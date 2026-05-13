from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, text, func
from .abstracciones.i_repository import IRepository
from models.practica_estrategia import PracticaEstrategia

class PracticaEstrategiaRepository(IRepository):

    def __init__(self, db: AsyncSession):
        self.db = db

    async def obtener_todos(self, esquema: str = None, limite: int = None):
        stmt = select(PracticaEstrategia)
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
        stmt = select(PracticaEstrategia).where(PracticaEstrategia.id == valor_id)
        result = await self.db.execute(stmt)
        fila = result.scalars().first()
        return fila.__dict__ if fila else None

    async def guardar(self, datos: dict, esquema: str = None):
        try:
            datos.pop('id', None)
            resultado = await self.db.execute(select(func.max(PracticaEstrategia.id)))
            max_id = resultado.scalar() or 0
            datos['id'] = max_id + 1

            entidad = PracticaEstrategia(**datos)
            self.db.add(entidad)
            await self.db.commit()
            return True, "Práctica/Estrategia guardada correctamente"
        except Exception as e:
            await self.db.rollback()
            print(f"ERROR REPO PRACTICA_ESTRATEGIA (GUARDAR): {e}")
            return False, f"Error: {str(e)}"

    async def actualizar(self, valor_id: int, datos: dict, esquema: str = None):
        try:
            datos.pop('id', None)
            stmt = update(PracticaEstrategia).where(
                PracticaEstrategia.id == valor_id
            ).values(**datos)
            result = await self.db.execute(stmt)
            await self.db.commit()
            if result.rowcount > 0:
                return True, "Práctica/Estrategia actualizada correctamente"
            return False, "No se encontró el registro"
        except Exception as e:
            await self.db.rollback()
            return False, f"Error al actualizar: {str(e)}"

    async def eliminar(self, entidad: dict, esquema: str = None):
        try:
            valor_id = entidad.get('id') if isinstance(entidad, dict) else entidad.id
            sql = text("DELETE FROM practica_estrategia WHERE id = :id_val")
            await self.db.execute(sql, {"id_val": valor_id})
            await self.db.commit()
            return True, "Práctica/Estrategia eliminada correctamente"
        except Exception as e:
            await self.db.rollback()
            return False, f"Error: {str(e)}"