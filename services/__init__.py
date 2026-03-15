# ─────────────────────────────────────────────────────────────
# __init__.py — Marca la carpeta "services" como un paquete Python.
#
# ¿Qué es un paquete Python?
# Es una carpeta que contiene archivos .py y un __init__.py.
# El __init__.py le dice a Python: "esta carpeta contiene código
# que se puede importar desde otros archivos".
#
# Sin este archivo, Python NO reconoce la carpeta como paquete
# y no podrías hacer: from services.api_service import ApiService
#
# ¿Qué hace "re-exportar"?
# Importamos ApiService aquí para que otros archivos puedan
# escribir: from services import ApiService
# en vez de: from services.api_service import ApiService
# Es un atajo de conveniencia.
# ─────────────────────────────────────────────────────────────

from .api_service import ApiService
# El punto (.) significa "desde esta misma carpeta".
# Sin el punto, Python buscaría "api_service" en todo el sistema.
# Con el punto, busca "api_service.py" dentro de services/.
