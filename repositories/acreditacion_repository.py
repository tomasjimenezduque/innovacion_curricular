from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, text
from .abstracciones.i_repository import IRepository
from models.acreditacion import Acreditacion

class AcreditacionRepository(IRepository):

    def __init__(self, db: AsyncSession):
        self.db = db

    async def obtener_todos(self, esquema: str = None, limite: int = None):
        stmt = select(Acreditacion)
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
        stmt = select(Acreditacion).where(Acreditacion.resolucion == valor_id)  # ← PK correcta
        result = await self.db.execute(stmt)
        fila = result.scalars().first()
        return fila.__dict__ if fila else None

    async def guardar(self, datos: dict, esquema: str = None):
        try:
            entidad = Acreditacion(**datos)
            self.db.add(entidad)
            await self.db.commit()
            return True, "Acreditación guardada correctamente"
        except Exception as e:
            await self.db.rollback()
            print(f"ERROR REPO ACREDITACION (GUARDAR): {e}")
            return False, f"Error: {str(e)}"

    async def actualizar(self, valor_id: int, datos: dict, esquema: str = None):
        try:
            datos.pop('resolucion', None)
            stmt = update(Acreditacion).where(
                Acreditacion.resolucion == valor_id  # ← PK correcta
            ).values(**datos)
            result = await self.db.execute(stmt)
            await self.db.commit()
            if result.rowcount > 0:
                return True, "Acreditación actualizada correctamente"
            return False, "No se encontró el registro"
        except Exception as e:
            await self.db.rollback()
            return False, f"Error al actualizar: {str(e)}"

    async def eliminar(self, entidad: dict, esquema: str = None):
        try:
            valor_id = entidad.get('resolucion') if isinstance(entidad, dict) else entidad.resolucion
            sql = text("DELETE FROM acreditacion WHERE resolucion = :r")
            await self.db.execute(sql, {"r": valor_id})
            await self.db.commit()
            return True, "Acreditación eliminada correctamente"
        except Exception as e:
            await self.db.rollback()
            return False, f"Error: {str(e)}"