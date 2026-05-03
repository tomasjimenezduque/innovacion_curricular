import requests
import logging
from config import API_BASE_URL
from services.abstracciones.i_api_service import IApiService

# Configuración de logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ApiService(IApiService):
    def __init__(self):
        # Aseguramos que la base_url sea limpia
        self.base_url = f"{API_BASE_URL}/api".rstrip('/')

    def _construir_url(self, tabla, valor_id=None):
        """Construye la URL siguiendo el estándar REST."""
        recurso = tabla.strip('/')
        if valor_id:
            # Importante: eliminamos espacios o slashes accidentales del ID
            return f"{self.base_url}/{recurso}/{str(valor_id).strip('/')}"
        return f"{self.base_url}/{recurso}/"

    def listar(self, tabla: str, esquema: str = None, limite: int = None):
        url = self._construir_url(tabla)
        params = {k: v for k, v in {"limite": limite, "esquema": esquema}.items() if v}
        try:
            # Usar un timeout es vital para no dejar colgada la app de Flask/FastAPI
            r = requests.get(url, params=params, timeout=5)
            if r.status_code == 204: 
                return []
            r.raise_for_status()
            datos = r.json()
            # Si el API devuelve el formato {"datos": [...]}, lo extraemos
            return datos if isinstance(datos, list) else datos.get("datos", [])
        except Exception as e:
            logger.error(f"❌ Error al listar {tabla} en {url}: {e}")
            return []

    def get(self, tabla, valor_id):
        if not valor_id: return None
        url = self._construir_url(tabla, valor_id)
        try:
            r = requests.get(url, timeout=5)
            if r.status_code == 200:
                return r.json()
            return None
        except Exception as e:
            logger.error(f"❌ Error en GET {url}: {e}")
            return None

    def crear(self, tabla: str, datos: dict, esquema: str = None):
        url = self._construir_url(tabla)
        try:
            r = requests.post(url, json=datos, timeout=5)
            # Intentar obtener mensaje de error del API si falla
            try:
                res_json = r.json()
                msg = res_json.get("mensaje") or res_json.get("detail") or "Operación realizada"
            except:
                msg = r.text or "Error desconocido"
                
            return r.status_code in (200, 201), msg
        except Exception as e:
            return False, f"Error de conexión: {str(e)}"

    def actualizar(self, tabla, clave_nombre, valor_id, datos, **kwargs):
        """
        RESTful Update: PUT /api/tabla/valor_id
        """
        url = self._construir_url(tabla, valor_id)
        try:
            r = requests.put(url, json=datos, timeout=5)
            try:
                res_json = r.json()
                # Buscamos 'mensaje' o 'detail' (estándar de FastAPI)
                msg = res_json.get("mensaje") or res_json.get("detail") or "Actualización exitosa"
            except:
                msg = "Error al procesar respuesta del servidor"

            return r.status_code == 200, msg
        except Exception as e:
            return False, f"Fallo de red: {str(e)}"

    def eliminar(self, recurso, valor_id, nombre_clave=None):
        """
        RESTful Delete: DELETE /api/recurso/valor_id
        """
        url = self._construir_url(recurso, valor_id)
        try:
            r = requests.delete(url, timeout=5)
            if r.status_code in (200, 204):
                return True, "Registro eliminado correctamente."
            
            # Intentar capturar por qué no se pudo eliminar (ej: integridad referencial)
            try:
                msg = r.json().get("detail", "No se pudo eliminar.")
            except:
                msg = f"Error {r.status_code} en el servidor."
                
            return False, msg
        except Exception as e:
            return False, f"Error de conexión: {str(e)}"

    # --- Métodos Compuestos (Mantener igual o ajustar según necesidad) ---

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