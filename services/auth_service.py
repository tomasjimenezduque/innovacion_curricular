"""
auth_service.py - Servicio de autenticacion contra la API generica FastAPI.

Usa el endpoint POST /api/{tabla}/verificar-contrasena de la API generica.
Sin JWT, sin consultas parametrizadas, sin descubrimiento de estructura.

FLUJO:
  1. Login: verifica email+contrasena via /api/usuario/verificar-contrasena
  2. Datos usuario: obtiene nombre desde GET /api/usuario
  3. Cambiar contrasena: PUT /api/usuario/email/{email}?campos_encriptar=contrasena
"""

import requests
from config import API_BASE_URL


class AuthService:
    """Servicio de autenticacion simple contra la API generica FastAPI."""

    def __init__(self):
        self.base_url = API_BASE_URL
        self.session = requests.Session()

    # ──────────────────────────────────────────────
    # LOGIN: POST /api/usuario/verificar-contrasena
    # ──────────────────────────────────────────────
    def login(self, email, contrasena):
        """
        Verifica credenciales contra la API generica.
        Retorna (True, {mensaje:...}) si OK, (False, {mensaje:...}) si falla.
        """
        try:
            url = f"{self.base_url}/api/usuario/verificar-contrasena"
            params = {
                "campo_usuario": "email",
                "campo_contrasena": "contrasena",
                "valor_usuario": email,
                "valor_contrasena": contrasena
            }
            resp = self.session.post(url, params=params, timeout=30)

            if resp.ok:
                return True, resp.json()
            return False, resp.json() if resp.text else {"mensaje": "Error de autenticacion."}
        except Exception as e:
            return False, {"mensaje": str(e)}

    # ──────────────────────────────────────────────
    # DATOS DEL USUARIO
    # ──────────────────────────────────────────────
    def obtener_datos_usuario(self, email):
        """Obtiene los datos del usuario buscando por email."""
        try:
            url = f"{self.base_url}/api/usuario/email/{email}"
            resp = self.session.get(url, timeout=30)
            if resp.ok:
                datos = resp.json().get("datos", [])
                if datos:
                    return datos[0]
        except Exception:
            pass
        return {}

    # ──────────────────────────────────────────────
    # CAMBIAR CONTRASENA
    # ──────────────────────────────────────────────
    def actualizar_contrasena(self, email, nueva_contrasena):
        """Actualiza la contrasena con encriptacion BCrypt."""
        try:
            url = f"{self.base_url}/api/usuario/email/{email}"
            params = {"campos_encriptar": "contrasena"}
            resp = self.session.put(
                url,
                json={"contrasena": nueva_contrasena},
                params=params,
                timeout=30
            )
            if resp.ok:
                return True, "Contrasena actualizada."
            msg = resp.json().get("mensaje", "Error al actualizar.") if resp.text else "Error al actualizar."
            return False, msg
        except Exception as e:
            return False, str(e)
