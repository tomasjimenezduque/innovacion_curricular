from sqlalchemy.orm import Session
from sqlalchemy import select, update
from .abstracciones.i_repository import IRepository
from models.alianza import Alianza

class AlianzaRepository(IRepository):

    def __init__(self, db: Session):
        self.db = db

    async def obtener_todos(self, esquema: str = None, limite: int = None):
        stmt = select(Alianza)
        if limite:
            stmt = stmt.limit(limite)
        
        result = self.db.execute(stmt)
        return result.scalars().all()

    async def obtener_por_id(self, valor_id: int, esquema: str = None):
        stmt = select(Alianza).where(Alianza.id == valor_id)
        result = self.db.execute(stmt)
        return result.scalars().first()

    async def guardar(self, entidad: Alianza, esquema: str = None):
        try:
            self.db.add(entidad)
            self.db.commit()
            self.db.refresh(entidad)
            return True, "Alianza guardada correctamente"
        except Exception as e:
            self.db.rollback()
            return False, f"Error: {str(e)}"

    async def actualizar(self, valor_id: int, datos: dict, esquema: str = None):
        """
        Actualiza una alianza estratégica.
        'datos' es el diccionario con los campos a modificar.
        """
        try:
            stmt = (
                update(Alianza)
                .where(Alianza.id == valor_id)
                .values(**datos)
            )
            
            result = self.db.execute(stmt)
            self.db.commit()
            
            if result.rowcount > 0:
                return True, "Alianza actualizada correctamente"
            return False, "No se encontró la alianza para actualizar"
        except Exception as e:
            self.db.rollback()
            return False, f"Error al actualizar la alianza: {str(e)}"

    async def eliminar(self, entidad: Alianza, esquema: str = None):
        try:
            self.db.delete(entidad)
            self.db.commit()
            return True, "Registro eliminado correctamente"
        except Exception as e:
            self.db.rollback()
            return False, f"Error: {str(e)}"