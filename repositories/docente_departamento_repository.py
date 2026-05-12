from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, text
from .abstracciones.i_repository import IRepository
from models.docente_departamento import DocenteDepartamento
import datetime

class DocenteDepartamentoRepository(IRepository):

    def __init__(self, db: AsyncSession):
        self.db = db

    async def obtener_todos(self, esquema: str = None, limite: int = None):
        stmt = select(DocenteDepartamento)
        if limite:
            stmt = stmt.limit(limite)
        result = await self.db.execute(stmt)
        filas = result.scalars().all()

        resultado_limpio = []
        for f in filas:
            d = f.__dict__.copy()
            d.pop('_sa_instance_state', None)
            if isinstance(d.get('fecha_ingreso'), (datetime.date, datetime.datetime)):
                d['fecha_ingreso'] = d['fecha_ingreso'].isoformat()
            if isinstance(d.get('fecha_salida'), (datetime.date, datetime.datetime)):
                d['fecha_salida'] = d['fecha_salida'].isoformat()
            resultado_limpio.append(d)
        return resultado_limpio

    async def obtener_por_id(self, docente_id: int, departamento_id: int, esquema: str = None):
        stmt = select(DocenteDepartamento).where(
            DocenteDepartamento.docente == docente_id,
            DocenteDepartamento.departamento == departamento_id
        )
        result = await self.db.execute(stmt)
        fila = result.scalars().first()
        return fila.__dict__ if fila else None

    async def guardar(self, datos: dict, esquema: str = None):
        try:
            if isinstance(datos.get('fecha_ingreso'), str):
                datos['fecha_ingreso'] = datetime.datetime.strptime(datos['fecha_ingreso'], '%Y-%m-%d').date()
            if datos.get('fecha_salida') and isinstance(datos['fecha_salida'], str):
                datos['fecha_salida'] = datetime.datetime.strptime(datos['fecha_salida'], '%Y-%m-%d').date()

            entidad = DocenteDepartamento(**datos)
            self.db.add(entidad)
            await self.db.commit()
            return True, "Asignación guardada correctamente"
        except Exception as e:
            await self.db.rollback()
            print(f"ERROR REPO DD (GUARDAR): {e}")
            return False, f"Error: {str(e)}"

    async def actualizar(self, docente_id: int, departamento_id: int, datos: dict, esquema: str = None):
        try:
            if isinstance(datos.get('fecha_ingreso'), str):
                datos['fecha_ingreso'] = datetime.datetime.strptime(datos['fecha_ingreso'], '%Y-%m-%d').date()
            if datos.get('fecha_salida') and isinstance(datos['fecha_salida'], str):
                datos['fecha_salida'] = datetime.datetime.strptime(datos['fecha_salida'], '%Y-%m-%d').date()

            stmt = (
                update(DocenteDepartamento)
                .where(
                    DocenteDepartamento.docente == docente_id,
                    DocenteDepartamento.departamento == departamento_id
                )
                .values(**datos)
            )
            result = await self.db.execute(stmt)
            await self.db.commit()

            if result.rowcount > 0:
                return True, "Asignación actualizada correctamente"
            return False, "No se encontró el registro"
        except Exception as e:
            await self.db.rollback()
            return False, f"Error al actualizar: {str(e)}"

    async def eliminar(self, docente_id: int, departamento_id: int, esquema: str = None):
        try:
            sql = text("DELETE FROM docente_departamento WHERE docente = :d AND departamento = :p")
            await self.db.execute(sql, {"d": docente_id, "p": departamento_id})
            await self.db.commit()
            return True, "Asignación eliminada correctamente"
        except Exception as e:
            await self.db.rollback()
            return False, f"Error al eliminar: {str(e)}"