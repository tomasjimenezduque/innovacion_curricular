from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, text
from .abstracciones.i_repository import IRepository
from models.aa_rc import AaRc

class AaRcRepository(IRepository):

    def __init__(self, db: AsyncSession):
        self.db = db

    async def obtener_todos(self, esquema: str = None, limite: int = None):
        stmt = select(AaRc)
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

    async def obtener_por_id(self, valor_id, esquema: str = None):
        return None

    async def obtener_por_llave_compuesta(self, id_curso: int, cod_reg: int, esquema: str = None):
        stmt = select(AaRc).where(
            AaRc.activ_academicas_idcurso == id_curso,      # ← nombre real
            AaRc.registro_calificado_codigo == cod_reg       # ← nombre real
        )
        result = await self.db.execute(stmt)
        fila = result.scalars().first()
        return fila.__dict__ if fila else None

    async def guardar(self, datos: dict, esquema: str = None):
        try:
            entidad = AaRc(**datos)
            self.db.add(entidad)
            await self.db.commit()
            return True, "Registro guardado correctamente"
        except Exception as e:
            await self.db.rollback()
            print(f"ERROR REPO AA_RC (GUARDAR): {e}")
            return False, f"Error: {str(e)}"

    async def actualizar(self, id_curso: int, cod_reg: int, datos: dict, esquema: str = None):
        try:
            stmt = update(AaRc).where(
                AaRc.activ_academicas_idcurso == id_curso,
                AaRc.registro_calificado_codigo == cod_reg
            ).values(**datos)
            result = await self.db.execute(stmt)
            await self.db.commit()
            if result.rowcount > 0:
                return True, "Registro actualizado correctamente"
            return False, "No se encontró el registro"
        except Exception as e:
            await self.db.rollback()
            return False, f"Error al actualizar: {str(e)}"

    async def eliminar(self, id_curso: int, cod_reg: int, esquema: str = None):
        try:
            sql = text("DELETE FROM aa_rc WHERE activ_academicas_idcurso = :c AND registro_calificado_codigo = :r")
            await self.db.execute(sql, {"c": id_curso, "r": cod_reg})
            await self.db.commit()
            return True, "Registro eliminado correctamente"
        except Exception as e:
            await self.db.rollback()
            return False, f"Error al eliminar: {str(e)}"