from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, text
from .abstracciones.i_repository import IRepository
from models.alianza import Alianza
import datetime

class AlianzaRepository(IRepository):

    def __init__(self, db: AsyncSession):
        self.db = db

    async def obtener_todos(self, esquema: str = None, limite: int = None):
        stmt = select(Alianza)
        if limite:
            stmt = stmt.limit(limite)
        result = await self.db.execute(stmt)
        filas = result.scalars().all()

        resultado_limpio = []
        for f in filas:
            d = f.__dict__.copy()
            d.pop('_sa_instance_state', None)
            if isinstance(d.get('fecha_inicio'), (datetime.date, datetime.datetime)):
                d['fecha_inicio'] = d['fecha_inicio'].isoformat()
            if isinstance(d.get('fecha_fin'), (datetime.date, datetime.datetime)):
                d['fecha_fin'] = d['fecha_fin'].isoformat()
            resultado_limpio.append(d)
        return resultado_limpio

    async def obtener_por_id(self, aliado_nit: str, departamento_id: int, esquema: str = None):
        stmt = select(Alianza).where(
            Alianza.aliado == aliado_nit,
            Alianza.departamento == departamento_id
        )
        result = await self.db.execute(stmt)
        fila = result.scalars().first()
        return fila.__dict__ if fila else None

    async def guardar(self, datos: dict, esquema: str = None):
        try:
            datos['aliado'] = str(datos['aliado'])
            if isinstance(datos.get('fecha_inicio'), str):
                datos['fecha_inicio'] = datetime.datetime.strptime(datos['fecha_inicio'], '%Y-%m-%d').date()
            if datos.get('fecha_fin') and isinstance(datos['fecha_fin'], str):
                datos['fecha_fin'] = datetime.datetime.strptime(datos['fecha_fin'], '%Y-%m-%d').date()

            entidad = Alianza(**datos)
            self.db.add(entidad)
            await self.db.commit()
            return True, "Alianza guardada correctamente"
        except Exception as e:
            await self.db.rollback()
            print(f"ERROR REPO ALIANZA (GUARDAR): {e}")
            return False, f"Error: {str(e)}"

    async def actualizar(self, aliado_nit: str, departamento_id: int, datos: dict, esquema: str = None):
        try:
            if isinstance(datos.get('fecha_inicio'), str):
                datos['fecha_inicio'] = datetime.datetime.strptime(datos['fecha_inicio'], '%Y-%m-%d').date()
            if datos.get('fecha_fin') and isinstance(datos['fecha_fin'], str):
                datos['fecha_fin'] = datetime.datetime.strptime(datos['fecha_fin'], '%Y-%m-%d').date()

            stmt = (
                update(Alianza)
                .where(
                    Alianza.aliado == aliado_nit,
                    Alianza.departamento == departamento_id
                )
                .values(**datos)
            )
            result = await self.db.execute(stmt)
            await self.db.commit()

            if result.rowcount > 0:
                return True, "Alianza actualizada correctamente"
            return False, "No se encontró la alianza"
        except Exception as e:
            await self.db.rollback()
            return False, f"Error al actualizar: {str(e)}"

    async def eliminar(self, aliado_nit: str, departamento_id: int, esquema: str = None):
        try:
            sql = text("DELETE FROM alianza WHERE aliado = :nit AND departamento = :dep")
            await self.db.execute(sql, {"nit": aliado_nit, "dep": departamento_id})
            await self.db.commit()
            return True, "Alianza eliminada correctamente"
        except Exception as e:
            await self.db.rollback()
            return False, f"Error al eliminar: {str(e)}"