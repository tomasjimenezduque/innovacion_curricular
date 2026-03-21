from abc import ABC, abstractmethod

class IApiService(ABC):
    @abstractmethod
    def listar(self, tabla: str, esquema: str = None, limite: int = None):
        """Para obtener todas las materias o registros"""
        pass

    @abstractmethod
    def crear(self, tabla: str, datos: dict, esquema: str = None):
        """Para insertar una nueva actividad académica"""
        pass

    @abstractmethod
    def eliminar_compuesto(self, tabla: str, id_1: int, id_2: int, esquema: str = None):
        """MÉTODO ESPECIAL: Para tu tabla aa_rc que no tiene un solo ID"""
        pass