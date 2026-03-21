from abc import ABC, abstractmethod

class IRepository(ABC):
    @abstractmethod
    async def listar(self, esquema: str | None = None, limite: int | None = None):
        pass

    @abstractmethod
    async def crear(self, datos: dict, esquema: str | None = None):
        pass

    @abstractmethod
    async def eliminar(self, id_curso: int, codigo_registro: int, esquema: str | None = None):
        pass