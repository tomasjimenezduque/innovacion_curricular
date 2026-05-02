from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, text
from .abstracciones.i_repository import IRepository
from models.facultad import Facultad
import datetime

class FacultadRepository(IRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def obtener_todos(self, esquema: str = None, limite: int = None):
        stmt = select(Facultad)
        result = await self.db.execute(stmt)
        filas = result.scalars().all()
    
        resultado_limpio = []
        for f in filas:
            d = f.__dict__.copy()
            d.pop('_sa_instance_state', None) # Quitar basura de SQLAlchemy
            # Convertimos la fecha a string para evitar el Error 500 de JSON
            if isinstance(d.get('fecha_fun'), (datetime.date, datetime.datetime)):
               d['fecha_fun'] = d['fecha_fun'].isoformat()
            resultado_limpio.append(d)
        
        return resultado_limpio

    async def obtener_por_id(self, valor_id: int, esquema: str = None):
        stmt = select(Facultad).where(Facultad.id == valor_id)
        result = await self.db.execute(stmt)
        fila = result.scalars().first()
        return fila.__dict__ if fila else None

    async def guardar(self, datos: dict, esquema: str = None):
        try:
            # Si el ID viene del front, lo quitamos para que sea autoincremental
            datos.pop('id', None)
        
            # Blindaje de fecha
            if isinstance(datos.get('fecha_fun'), str):
                datos['fecha_fun'] = datetime.datetime.strptime(datos['fecha_fun'], '%Y-%m-%d').date()
            
            nueva_entidad = Facultad(**datos)
            self.db.add(nueva_entidad)
            await self.db.commit()
            return True, "Guardado con éxito"
        except Exception as e:
            await self.db.rollback()
            print(f"Error específico: {e}") # Mira esto en tu terminal
            return False, str(e)

    async def actualizar(self, valor_id: int, datos: dict, esquema: str = None):
        try:
            # 1. Limpieza de datos (ID no se actualiza manualmente)
            datos.pop('id', None)

            # 2. Blindaje de fecha: Convertir string del HTML a objeto date de Python
            if isinstance(datos.get('fecha_fun'), str):
                try:
                    datos['fecha_fun'] = datetime.datetime.strptime(datos['fecha_fun'], '%Y-%m-%d').date()
                except ValueError:
                    return False, "Formato de fecha inválido. Use YYYY-MM-DD"

            # 3. Ejecución del Update
            stmt = (
                update(Facultad)
                .where(Facultad.id == valor_id)
                .values(**datos)
            )
            
            result = await self.db.execute(stmt)
            await self.db.commit()

            if result.rowcount == 0:
                return False, "No se encontró la facultad para actualizar"

            return True, "Facultad actualizada correctamente"

        except Exception as e:
            await self.db.rollback()
            print(f"Error en actualización: {e}")
            return False, str(e)

    async def eliminar(self, entidad: any, esquema: str = None):
        try:
            # Usamos el ID del objeto que nos pasa el Router
            valor_id = entidad.get('id') if isinstance(entidad, dict) else entidad.id
            sql = text("DELETE FROM facultad WHERE id = :id_val")
            await self.db.execute(sql, {"id_val": valor_id})
            await self.db.commit()
            return True, "Facultad eliminada"
        except Exception as e:
            await self.db.rollback()
            return False, f"Error (Dependencias activas?): {str(e)}"