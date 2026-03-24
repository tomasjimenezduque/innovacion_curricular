from abc import ABC, abstractmethod
from typing import Any, Optional, List

class IRepository(ABC):

    @abstractmethod
    async def obtener_todos(self, esquema: Optional[str] = None, limite: Optional[int] = None) -> List[Any]:
        """Retorna una lista de todas las entidades."""
        pass

    @abstractmethod
    async def obtener_por_id(self, valor_id: Any, esquema: Optional[str] = None) -> Optional[Any]:
        """Busca una entidad por su llave primaria (sea id, codigo, etc)."""
        pass

    @abstractmethod
    async def actualizar(self, valor_id: Any, datos: dict, esquema: Optional[str] = None) -> Any:
        """
        Actualiza una entidad existente usando un diccionario de cambios.
        Retorna la entidad actualizada o el número de filas afectadas.
        """
        pass
    
    @abstractmethod
    async def guardar(self, entidad: Any, esquema: Optional[str] = None) -> tuple[bool, str]:
        """Crea o actualiza una instancia del modelo de SQLAlchemy."""
        pass

    @abstractmethod
    async def eliminar(self, entidad: Any, esquema: Optional[str] = None) -> tuple[bool, str]:
        """Elimina una instancia física de la base de datos."""
        pass 