"""Middleware de autenticacion simplificado (sin JWT, sin roles/rutas dinamicos).

Verifica solo si el usuario tiene sesion activa.
Las rutas publicas (/login, /logout, /static) no requieren sesion.
"""

from flask import session, redirect, url_for, request, render_template


RUTAS_PUBLICAS = ['/login', '/logout', '/static', '/recuperar-contrasena']


def crear_middleware(app):
    """Registra before_request y context_processor."""

    @app.before_request
    def verificar_autenticacion():
        # Auth desactivado para desarrollo sin base de datos de usuarios
        return

    @app.context_processor
    def inyectar_sesion():
        return {
            "usuario": session.get("usuario", ""),
            "nombre_usuario": session.get("nombre_usuario", ""),
        }
