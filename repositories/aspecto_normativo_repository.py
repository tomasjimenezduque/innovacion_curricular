from sqlalchemy.orm import Session
from sqlalchemy import select, update
from .abstracciones.i_repository import IRepository
from models.aspecto_normativo import AspectoNormativo

class AspectoNormativoRepository(IRepository):

    def __init__(self, db: Session):
        self.db = db

    async def obtener_todos(self, esquema: str = None, limite: int = None):
        stmt = select(AspectoNormativo)
        if limite:
            stmt = stmt.limit(limite)
        
        result = self.db.execute(stmt)
        return result.scalars().all()

    async def obtener_por_id(self, valor_id: int, esquema: str = None):
        stmt = select(AspectoNormativo).where(AspectoNormativo.id == valor_id)
        result = self.db.execute(stmt)
        return result.scalars().first()

    async def guardar(self, entidad: AspectoNormativo, esquema: str = None):
        try:
            self.db.add(entidad)
            self.db.commit()
            self.db.refresh(entidad)
            return True, "Registro guardado correctamente"
        except Exception as e:
            self.db.rollback()
            return False, f"Error: {str(e)}"

    async def actualizar(self, valor_id: int, datos: dict, esquema: str = None):
        """
        Actualiza un aspecto normativo existente.
        'datos' es el diccionario con los campos a modificar.
        """
        try:
            stmt = (
                update(AspectoNormativo)
                .where(AspectoNormativo.id == valor_id)
                .values(**datos)
            )
            
            result = self.db.execute(stmt)
            self.db.commit()
            
            if result.rowcount > 0:
                return True, "Aspecto normativo actualizado correctamente"
            return False, "No se encontró el registro para actualizar"
        except Exception as e:
            self.db.rollback()
            return False, f"Error al actualizar: {str(e)}"

    async def eliminar(self, entidad: AspectoNormativo, esquema: str = None):
        try:
            self.db.delete(entidad)
            self.db.commit()
            return True, "Registro eliminado correctamente"
        except Exception as e:
            self.db.rollback()
            return False, f"Error: {str(e)}"
