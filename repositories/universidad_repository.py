from sqlalchemy.ext.asyncio import AsyncSession # Cambio a sesión asíncrona
from sqlalchemy.orm import selectinload
from sqlalchemy import select, update, text
from .abstracciones.i_repository import IRepository
from models.universidad import Universidad

class UniversidadRepository(IRepository):

    def __init__(self, db: AsyncSession): # Inyectamos AsyncSession
        self.db = db

    async def obtener_todos(self, esquema: str = None, limite: int = None):
        """Lista todas las universidades registradas."""
        stmt = select(Universidad)
        if limite:
            stmt = stmt.limit(limite)
        
        # CORRECCIÓN: await para ejecución asíncrona
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def obtener_por_id(self, valor_id: int, esquema: str = None):
        """
        Obtiene una universidad y sus facultades asociadas.
        """
        # CORRECCIÓN: Usamos selectinload para cargar la colección de facultades
        stmt = select(Universidad).where(Universidad.id == valor_id).options(
            selectinload(Universidad.facultad)
        )
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def guardar(self, datos: dict, esquema: str = None): # Recibimos dict
        try:
            # Convertimos el diccionario en una instancia del Modelo
            nueva_universidad = Universidad(**datos) 
        
            self.db.add(nueva_universidad)
            await self.db.commit()
            await self.db.refresh(nueva_universidad)
            return True, "Universidad guardada correctamente"
        except Exception as e:
            await self.db.rollback()
            # Esto te dirá en el log exactamente qué campo falla
            print(f"DEBUG ERROR REPO: {str(e)}") 
            return False, f"Error: {str(e)}"

    async def actualizar(self, valor_id: int, datos: dict, esquema: str = None):
        """
        Actualiza los datos de la institución.
        """
        try:
            stmt = (
                update(Universidad)
                .where(Universidad.id == valor_id)
                .values(**datos)
            )
            # CORRECCIÓN: await en execute y commit
            result = await self.db.execute(stmt)
            await self.db.commit()
            
            if result.rowcount > 0:
                return True, "Universidad actualizada con éxito"
            return False, "No se encontró la universidad para actualizar"
        except Exception as e:
            await self.db.rollback()
            return False, f"Error al actualizar: {str(e)}"

    async def eliminar(self, id_u: int):
        # Envolvemos el SQL en la función text()
        sql = text("DELETE FROM universidad WHERE id = :id_val")
    
        try:
        # Ejecutamos pasando el parámetro como un diccionario
            await self.db.execute(sql, {"id_val": id_u})
            await self.db.commit() # ¡No olvides el commit!
        
            return True, "Registro eliminado correctamente."
        except Exception as e:
            await self.db.rollback() # Si falla, volvemos atrás
            print(f"Error en SQL eliminar: {e}")
            return False, str(e)