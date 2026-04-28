import requests
from config import API_BASE_URL
from .abstracciones.i_api_service import IApiService

class ApiService(IApiService):
    def __init__(self):
        self.base_url = f"{API_BASE_URL}/api"

    def listar(self, tabla, esquema=None, limite=None):
        url = f"{self.base_url}/{tabla}/"
        params = {}
        if limite: params["limite"] = limite
        if esquema: params["esquema"] = esquema

        try:
            respuesta = requests.get(url, params=params)
            if respuesta.status_code == 204:
                return []
            datos = respuesta.json()
            return datos.get("datos", [])
        except Exception as e:
            print(f"[ERROR] Listar {tabla}: {e}")
            return []

    def get(self, tabla, valor_clave):
        """
        Obtiene un registro específico por su ID.
        Fundamental para que 'universidad_editar' no sea None.
        """
        url = f"{self.base_url}/{tabla}/{valor_clave}"
        try:
            respuesta = requests.get(url)
            if respuesta.status_code == 200:
                # Retorna directamente el objeto del registro
                return respuesta.json()
            return None
        except Exception as e:
            print(f"[ERROR] Get {tabla}/{valor_clave}: {e}")
            return None

    def crear(self, tabla, datos, esquema=None, **kwargs):
        url = f"{self.base_url}/{tabla}/"
        try:
            respuesta = requests.post(url, json=datos)
            cuerpo = respuesta.json()

            if respuesta.status_code in (200, 201):
                return True, cuerpo.get("mensaje", "Registro creado.")
            
            detalle = cuerpo.get("detail", "Error en la operación")
            return False, f"Error: {detalle}"
        except Exception as e:
            return False, f"Error de conexión: {e}"

    def actualizar(self, tabla, clave_nombre, valor_clave, datos, **kwargs):
        url = f"{self.base_url}/{tabla}/{valor_clave}"
        try:
            respuesta = requests.put(url, json=datos)
            cuerpo = respuesta.json()

            if respuesta.status_code == 200:
                return True, cuerpo.get("mensaje", "Registro actualizado.")
            
            detalle = cuerpo.get("detail", "Error al actualizar")
            return False, f"Error: {detalle}"
        except Exception as e:
            return False, f"Error de conexión: {e}"

    def eliminar(self, tabla, clave_nombre, valor_clave):
        url = f"{self.base_url}/{tabla}/{valor_clave}"
        try:
            respuesta = requests.delete(url)
            cuerpo = respuesta.json()
            if respuesta.status_code == 200:
                return True, cuerpo.get("mensaje", "Registro eliminado.")
            return False, cuerpo.get("detail", "Error al eliminar")
        except Exception as e:
            return False, f"Error de conexión: {e}"

    # --- Métodos para tablas intermedias (Asociaciones) ---
    def actualizar_compuesto(self, tabla, id1, id2, datos, esquema=None):
        url = f"{self.base_url}/{tabla}/{id1}/{id2}"
        try:
            respuesta = requests.put(url, json=datos)
            return respuesta.status_code == 200, respuesta.json().get("mensaje", "")
        except Exception as e:
            return False, str(e)

    def eliminar_compuesto(self, tabla, id1, id2, esquema=None):
        url = f"{self.base_url}/{tabla}/{id1}/{id2}"
        try:
            respuesta = requests.delete(url)
            return respuesta.status_code == 200, respuesta.json().get("mensaje", "")
        except Exception as e:
            return False, str(e)