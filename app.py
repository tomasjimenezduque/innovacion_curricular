"""
app.py — Punto de entrada del frontend Flask.

Este es el PRIMER archivo que se ejecuta cuando inicias el frontend.
Su responsabilidad es:
1. Crear la aplicación Flask (el "servidor web" que muestra las páginas)
2. Configurar la clave secreta (para sesiones y mensajes flash)
3. Registrar los Blueprints (grupos de rutas/páginas)

Para ejecutar:
    python app.py

Después, abre tu navegador en: http://localhost:5100

────────────────────────────────────────────────────────────────
CONCEPTO CLAVE: ¿Qué es Flask?
────────────────────────────────────────────────────────────────
Flask es un framework web. Un framework web hace esto:

    1. El usuario escribe una URL en el navegador (ej: localhost:5100/producto)
    2. Flask recibe esa petición
    3. Flask busca qué función de Python maneja esa URL
    4. Esa función genera una página HTML
    5. Flask envía el HTML al navegador
    6. El navegador muestra la página

Es como un restaurante:
    - El cliente (navegador) hace un pedido (URL)
    - El mesero (Flask) lleva el pedido a la cocina (tu código Python)
    - La cocina prepara el plato (genera HTML)
    - El mesero lleva el plato al cliente (respuesta HTTP)
────────────────────────────────────────────────────────────────
"""

# ─── Imports ─────────────────────────────────────────────────

from flask import Flask
# Flask: la clase principal. Crear Flask(__name__) es crear tu
# aplicación web. __name__ le dice a Flask dónde están los archivos
# del proyecto (templates, static, etc.).

from config import SECRET_KEY
# Importa la clave secreta desde config.py.
# La necesitamos para que Flask pueda firmar las cookies de sesión.

from routes.home import home_bp
from routes.producto import producto_bp
from routes.universidad import  universidad_bp
# Importa los Blueprints (grupos de rutas).
# home_bp     → maneja la página principal (/)
# producto_bp → maneja las páginas de producto (/producto, /producto/crear, etc.)
#
# ¿Qué es un Blueprint?
# Es una forma de organizar las rutas en archivos separados.
# Sin Blueprints, TODAS las rutas estarían en app.py (un archivo enorme).
# Con Blueprints, cada "sección" de la web tiene su propio archivo.

from routes.acreditacion import acreditacion_bp

from routes.activ_academica import activ_academica_bp

from routes.aliado import aliado_bp

# ─── Crear la aplicación Flask ───────────────────────────────

app = Flask(__name__)
# Crea la instancia de Flask.
# __name__ = nombre del módulo actual ("__main__" cuando se ejecuta directamente).
# Flask usa __name__ para encontrar la carpeta del proyecto y así localizar:
#   - templates/  → las plantillas HTML
#   - static/     → archivos CSS, JS, imágenes

app.secret_key = SECRET_KEY
# Configura la clave secreta.
# Sin esta línea, Flask NO puede usar:
#   - flash() → mensajes de éxito/error entre páginas
#   - session → datos temporales del usuario


# ─── Registrar Blueprints (grupos de rutas) ──────────────────

app.register_blueprint(home_bp)
# Registra las rutas del home. Después de esta línea,
# Flask sabe que cuando alguien visite "/" debe usar home_bp.

app.register_blueprint(producto_bp)
# Registra las rutas de producto. Después de esta línea,
# Flask sabe que las URLs /producto, /producto/crear, etc.
# deben usar producto_bp.
#
# PARA AGREGAR MÁS PÁGINAS EN EL FUTURO:
# 1. Crea un nuevo archivo en routes/ (ej: routes/empresa.py)
# 2. Define un Blueprint en ese archivo
# 3. Importa el Blueprint aquí
# 4. Registra con app.register_blueprint(empresa_bp)
app.register_blueprint(universidad_bp)

app.register_blueprint(acreditacion_bp)


app.register_blueprint(activ_academica_bp, url_prefix='/activ_academica')

app.register_blueprint(aliado_bp, url_prefix='/aliado')


# ─── Ejecutar el servidor ────────────────────────────────────

if __name__ == "__main__":
    # __name__ == "__main__" solo es True cuando ejecutas:
    #   python app.py
    # NO es True cuando otro archivo importa app.py.
    # Esto evita que el servidor se inicie accidentalmente al importar.

    # ─── Usamos Waitress en vez del servidor de desarrollo de Flask ───
    # El servidor de Flask (app.run) es MUY lento porque:
    #   - Es mono-hilo (atiende UNA petición a la vez)
    #   - Está diseñado para desarrollo, NO para rendimiento
    #
    # Waitress es un servidor WSGI rápido y multi-hilo:
    #   - Atiende MÚLTIPLES peticiones simultáneamente
    #   - Funciona perfecto en Windows (a diferencia de gunicorn)
    #   - Es estable y seguro para producción
    # ──────────────────────────────────────────────────────────────────
    from waitress import serve

    print(" * Frontend Flask corriendo en: http://127.0.0.1:5200")
    print(" * Servidor: Waitress (multi-hilo)")
    print(" * Presiona Ctrl+C para detener")

    serve(
        app,
        host="127.0.0.1",  # Solo acepta conexiones locales
        port=5200,          # Puerto del frontend
        threads=4           # 4 hilos para atender peticiones en paralelo
    )
