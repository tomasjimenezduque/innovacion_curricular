import requests
import logging
from config import API_BASE_URL
from services.abstracciones.i_api_service import IApiService

# Configuración de logs para depuración
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ApiService(IApiService):
    def __init__(self):
        # Aseguramos que la base_url no termine en / para manejarlo manualmente
        self.base_url = f"{API_BASE_URL}/api".rstrip('/')

    def _construir_url(self, tabla, valor_id=None):
        """
        Construye la URL de forma limpia. 
        Si hay valor_id: /api/tabla/id
        Si no: /api/tabla/
        """
        recurso = tabla.strip('/')
        if valor_id:
            # Importante: No ponemos / al final si hay un ID (estándar REST)
            return f"{self.base_url}/{recurso}/{str(valor_id).strip('/')}"
        return f"{self.base_url}/{recurso}/"

    def listar(self, tabla: str, esquema: str = None, limite: int = None):
        url = self._construir_url(tabla)
        params = {k: v for k, v in {"limite": limite, "esquema": esquema}.items() if v}
        try:
            r = requests.get(url, params=params, timeout=5)
            if r.status_code == 204: return []
            r.raise_for_status()
            datos = r.json()
            # Retorna la lista de 'datos' o el json directo si es una lista
            return datos if isinstance(datos, list) else datos.get("datos", [])
        except Exception as e:
            logger.error(f"Error al listar {tabla}: {e}")
            return []

    def get(self, tabla, valor_id):
        """Recupera un solo registro por su ID."""
        if not valor_id: return None
        url = self._construir_url(tabla, valor_id)
        try:
            r = requests.get(url, timeout=5)
            if r.status_code == 200:
                return r.json()
            return None
        except Exception as e:
            logger.error(f"Error en GET {tabla}/{valor_id}: {e}")
            return None

    def crear(self, tabla: str, datos: dict, esquema: str = None):
        url = self._construir_url(tabla)
        try:
            r = requests.post(url, json=datos, timeout=5)
            # Manejamos posibles errores del API (400, 500, etc)
            respuesta = r.json() if r.status_code in (200, 201) else {"mensaje": r.text}
            return r.status_code in (200, 201), respuesta.get("mensaje", "Registro creado.")
        except Exception as e:
            return False, f"Error de conexión: {str(e)}"

    def actualizar(self, tabla, clave_nombre, valor_id, datos, **kwargs):
        """
        En REST, el ID va en la URL. 
        'clave_nombre' se mantiene por compatibilidad con la interfaz.
        """
        url = self._construir_url(tabla, valor_id)
        try:
            r = requests.put(url, json=datos, timeout=5)
            if r.status_code == 200:
                return True, r.json().get("mensaje", "Actualización exitosa.")
            # Si da 404 o 405, el mensaje de error vendrá del API
            msg = r.json().get("detail", "Error al actualizar") if r.status_code != 500 else "Error interno del servidor"
            return False, msg
        except Exception as e:
            return False, str(e)

    def eliminar(self, recurso, nombre_clave, valor_id):
        url = self._construir_url(recurso, valor_id)
        try:
            r = requests.delete(url, timeout=5)
            return r.status_code in (200, 204), "Eliminado correctamente."
        except Exception as e:
            return False, str(e)

    # --- Métodos Compuestos ---

    def eliminar_compuesto(self, tabla: str, id_1: int, id_2: int, esquema: str = None):
        url = f"{self.base_url}/{tabla.strip('/')}/{id_1}/{id_2}"
        try:
            r = requests.delete(url, timeout=5)
            return r.status_code in (200, 204), "Vínculo eliminado."
        except Exception as e:
            return False, str(e)

    def actualizar_compuesto(self, tabla: str, id_1: int, id_2: int, datos: dict, esquema: str = None):
        url = f"{self.base_url}/{tabla.strip('/')}/{id_1}/{id_2}"
        try:
            r = requests.put(url, json=datos, timeout=5)
            return r.status_code == 200, r.json().get("mensaje", "Vínculo actualizado.")
        except Exception as e:
            return False, str(e)