# api_service.py — Clase genérica para comunicarse con la API backend.

# ─── Imports ─────────────────────────────────────────────────
import requests
from config import API_BASE_URL
from .abstracciones.i_api_service import IApiService  # <--- IMPORTAMOS LA INTERFAZ

class ApiService(IApiService): # <--- AQUÍ HEREDAMOS
    """
    Servicio genérico para operaciones CRUD contra la API FastAPI.
    Implementa la interfaz IApiService.
    """

    def __init__(self):
        """
        Constructor: se ejecuta al crear la instancia.
        """
        self.base_url = f"{API_BASE_URL}/api"

    # ═══════════════════════════════════════════════════════════
    #  LISTAR — Obtener todos los registros de una tabla
    # ═══════════════════════════════════════════════════════════
    def listar(self, tabla, esquema=None, limite=None):
        url = f"{self.base_url}/{tabla}/"
        params = {}
        if limite:
            params["limite"] = limite

        try:
            respuesta = requests.get(url, params=params)
            datos = respuesta.json()
            return datos.get("datos", [])
        except requests.RequestException as e:
            print(f"[ERROR] No se pudo conectar a la API: {e}")
            return []

    # ═══════════════════════════════════════════════════════════
    #  OBTENER — Obtener UN solo registro por su clave
    # ═══════════════════════════════════════════════════════════
    def obtener(self, tabla, valor_clave):
        url = f"{self.base_url}/{tabla}/{valor_clave}"
        try:
            respuesta = requests.get(url)
            if respuesta.status_code == 200:
                datos = respuesta.json()
                lista = datos.get("datos", [])
                if lista:
                    return lista[0]
            return None
        except requests.RequestException as e:
            print(f"[ERROR] No se pudo obtener registro: {e}")
            return None

    # ═══════════════════════════════════════════════════════════
    #  CREAR — Crear un nuevo registro
    # ═══════════════════════════════════════════════════════════
    def crear(self, tabla, datos, esquema=None):
        url = f"{self.base_url}/{tabla}/"
        try:
            respuesta = requests.post(url, json=datos)
            cuerpo = respuesta.json()

            if respuesta.status_code in (200, 201):
                mensaje = cuerpo.get("mensaje", "Registro creado.")
                return (True, mensaje)
            else:
                detalle = cuerpo.get("detail", cuerpo.get("mensaje", ""))
                mensaje = str(detalle.get("mensaje", detalle) if isinstance(detalle, dict) else detalle)
                return (False, f"Error: {mensaje}")
        except requests.RequestException as e:
            return (False, f"Error de conexión: {e}")

    # ═══════════════════════════════════════════════════════════
    #  ACTUALIZAR — Modificar un registro existente (Compuesto)
    # ═══════════════════════════════════════════════════════════
    def actualizar_compuesto(self, tabla, id1, id2, datos, esquema=None):
        """Implementación del contrato para llaves compuestas"""
        url = f"{self.base_url}/{tabla}/{id1}/{id2}"
        try:
            respuesta = requests.put(url, json=datos)
            cuerpo = respuesta.json()
            if respuesta.status_code == 200:
                return True, cuerpo.get("mensaje", "Actualizado")
            return False, cuerpo.get("mensaje", "Error")
        except requests.RequestException as e:
            return False, str(e)

    # ═══════════════════════════════════════════════════════════
    #  ELIMINAR — Borrar un registro (Compuesto)
    # ═══════════════════════════════════════════════════════════
    def eliminar_compuesto(self, tabla, id1, id2, esquema=None):
        """Implementación del contrato para eliminar en tablas como aa_rc"""
        url = f"{self.base_url}/{tabla}/{id1}/{id2}"
        try:
            respuesta = requests.delete(url)
            cuerpo = respuesta.json()
            return respuesta.status_code == 200, cuerpo.get("mensaje", "")
        except requests.RequestException as e:
            return False, str(e)

    # Métodos legacy/simples para compatibilidad
    def actualizar(self, tabla, valor_clave, datos):
        url = f"{self.base_url}/{tabla}/{valor_clave}"
        try:
            respuesta = requests.put(url, json=datos)
            cuerpo = respuesta.json()
            return respuesta.status_code == 200, cuerpo.get("mensaje", "Registro actualizado.")
        except requests.RequestException as e:
            return False, f"Error de conexión: {e}"

    def eliminar(self, tabla, valor_clave):
        url = f"{self.base_url}/{tabla}/{valor_clave}"
        try:
            respuesta = requests.delete(url)
            cuerpo = respuesta.json()
            return respuesta.status_code == 200, cuerpo.get("mensaje", "Registro eliminado.")
        except requests.RequestException as e:
            return False, f"Error de conexión: {e}"