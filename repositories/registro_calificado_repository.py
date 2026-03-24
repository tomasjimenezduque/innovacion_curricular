from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select, update
from .abstracciones.i_repository import IRepository
from models.registro_calificado import RegistroCalificado

class RegistroCalificadoRepository(IRepository):

    def __init__(self, db: Session):
        self.db = db

    async def obtener_todos(self, esquema: str = None, limite: int = None):
        """Lista los registros cargando el programa asociado para evitar N+1."""
        stmt = select(RegistroCalificado).options(joinedload(RegistroCalificado.programa_))
        if limite:
            stmt = stmt.limit(limite)
        
        result = self.db.execute(stmt)
        return result.scalars().all()

    async def obtener_por_id(self, valor_id: int, esquema: str = None):
        """Busca por el campo 'codigo' y carga enfoques y actividades."""
        stmt = (
            select(RegistroCalificado)
            .where(RegistroCalificado.codigo == valor_id)
            .options(
                joinedload(RegistroCalificado.enfoque),
                joinedload(RegistroCalificado.aa_rc)
            )
        )
        result = self.db.execute(stmt)
        return result.scalars().first()

    async def guardar(self, entidad: RegistroCalificado, esquema: str = None):
        try:
            self.db.add(entidad)
            self.db.commit()
            self.db.refresh(entidad)
            return True, "Registro Calificado guardado correctamente"
        except Exception as e:
            self.db.rollback()
            return False, f"Error: {str(e)}"

    async def actualizar(self, codigo: int, datos: dict, esquema: str = None):
        """
        Actualización directa por código usando el estándar de SQLAlchemy 2.0.
        Retorna un booleano y un mensaje para consistencia con el resto del proyecto.
        """
        try:
            stmt = (
                update(RegistroCalificado)
                .where(RegistroCalificado.codigo == codigo)
                .values(**datos)
            )
            result = self.db.execute(stmt)
            self.db.commit()
            
            if result.rowcount > 0:
                return True, "Registro Calificado actualizado correctamente"
            return False, "No se encontró el registro para actualizar"
        except Exception as e:
            self.db.rollback()
            return False, f"Error al actualizar: {str(e)}"

    async def eliminar(self, entidad: RegistroCalificado, esquema: str = None):
        try:
            self.db.delete(entidad)
            self.db.commit()
            return True, "Registro Calificado eliminado"
        except Exception as e:
            self.db.rollback()
            return False, f"Error: {str(e)}"