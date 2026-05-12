from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, text
from .abstracciones.i_repository import IRepository
from models.registro_calificado import RegistroCalificado
import datetime

class RegistroCalificadoRepository(IRepository):

    def __init__(self, db: AsyncSession):
        self.db = db

    async def obtener_todos(self, esquema: str = None, limite: int = None):
        stmt = select(RegistroCalificado)
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

    async def obtener_por_id(self, valor_id: int, esquema: str = None):
        stmt = select(RegistroCalificado).where(RegistroCalificado.codigo == valor_id)
        result = await self.db.execute(stmt)
        fila = result.scalars().first()
        return fila.__dict__ if fila else None

    async def guardar(self, datos: dict, esquema: str = None):
        try:
            if isinstance(datos.get('fecha_inicio'), str):
                datos['fecha_inicio'] = datetime.datetime.strptime(datos['fecha_inicio'], '%Y-%m-%d').date()
            if isinstance(datos.get('fecha_fin'), str):
                datos['fecha_fin'] = datetime.datetime.strptime(datos['fecha_fin'], '%Y-%m-%d').date()

            entidad = RegistroCalificado(**datos)
            self.db.add(entidad)
            await self.db.commit()
            return True, "Registro Calificado guardado correctamente"
        except Exception as e:
            await self.db.rollback()
            print(f"ERROR REPO RC (GUARDAR): {e}")
            return False, f"Error: {str(e)}"

    async def actualizar(self, codigo: int, datos: dict, esquema: str = None):
        try:
            datos.pop('codigo', None)
            if isinstance(datos.get('fecha_inicio'), str):
                datos['fecha_inicio'] = datetime.datetime.strptime(datos['fecha_inicio'], '%Y-%m-%d').date()
            if isinstance(datos.get('fecha_fin'), str):
                datos['fecha_fin'] = datetime.datetime.strptime(datos['fecha_fin'], '%Y-%m-%d').date()

            stmt = update(RegistroCalificado).where(
                RegistroCalificado.codigo == codigo
            ).values(**datos)
            result = await self.db.execute(stmt)
            await self.db.commit()

            if result.rowcount > 0:
                return True, "Registro Calificado actualizado correctamente"
            return False, "No se encontró el registro"
        except Exception as e:
            await self.db.rollback()
            return False, f"Error al actualizar: {str(e)}"

    async def eliminar(self, entidad: dict, esquema: str = None):
        try:
            codigo = entidad.get('codigo') if isinstance(entidad, dict) else entidad.codigo
            sql = text("DELETE FROM registro_calificado WHERE codigo = :cod")
            await self.db.execute(sql, {"cod": codigo})
            await self.db.commit()
            return True, "Registro Calificado eliminado"
        except Exception as e:
            await self.db.rollback()
            return False, f"Error: {str(e)}"