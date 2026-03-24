from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select, update
from .abstracciones.i_repository import IRepository
from models.rol import Rol

class RolRepository(IRepository):

    def __init__(self, db: Session):
        self.db = db

    async def obtener_todos(self, esquema: str = None, limite: int = None):
        """Lista todos los roles disponibles en el sistema."""
        stmt = select(Rol)
        if limite:
            stmt = stmt.limit(limite)
        
        result = self.db.execute(stmt)
        return result.scalars().all()

    async def obtener_por_id(self, valor_id: int, esquema: str = None):
        """Obtiene un rol específico y sus usuarios asociados."""
        stmt = select(Rol).where(Rol.id == valor_id).options(
            joinedload(Rol.usuario)
        )
        result = self.db.execute(stmt)
        return result.scalars().first()

    async def guardar(self, entidad: Rol, esquema: str = None):
        try:
            self.db.add(entidad)
            self.db.commit()
            self.db.refresh(entidad)
            return True, "Rol guardado correctamente"
        except Exception as e:
            self.db.rollback()
            return False, f"Error: {str(e)}"

    async def actualizar(self, valor_id: int, datos: dict, esquema: str = None):
        """
        Actualiza los datos de un rol (ej. cambiar el nombre de 'Admin' a 'SuperAdmin').
        """
        try:
            stmt = (
                update(Rol)
                .where(Rol.id == valor_id)
                .values(**datos)
            )
            result = self.db.execute(stmt)
            self.db.commit()
            
            if result.rowcount > 0:
                return True, "Rol actualizado correctamente"
            return False, "No se encontró el rol para actualizar"
        except Exception as e:
            self.db.rollback()
            return False, f"Error al actualizar: {str(e)}"

    async def eliminar(self, entidad: Rol, esquema: str = None):
        try:
            # Nota: Si el rol tiene usuarios vinculados, PostgreSQL lanzará un error de FK
            self.db.delete(entidad)
            self.db.commit()
            return True, "Rol eliminado correctamente"
        except Exception as e:
            self.db.rollback()
            return False, f"Error: {str(e)}"

    async def obtener_por_nombre(self, nombre: str):
        """Útil para validaciones de seguridad o inyección de roles iniciales."""
        stmt = select(Rol).where(Rol.nombre == nombre)
        result = self.db.execute(stmt)
        return result.scalars().first()