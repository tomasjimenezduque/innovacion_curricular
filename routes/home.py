"""
home.py — Ruta para la página de inicio (Home).

Esta es la página más simple del proyecto. Solo muestra
un mensaje de bienvenida y un resumen de lo que hace la aplicación.

────────────────────────────────────────────────────────────────
CONCEPTO CLAVE: ¿Qué es un Blueprint?
────────────────────────────────────────────────────────────────
Un Blueprint es un "módulo" de Flask que agrupa rutas relacionadas.

Sin Blueprint:
    @app.route("/")           ← todo en app.py
    @app.route("/producto")   ← todo en app.py
    @app.route("/empresa")    ← todo en app.py
    (un archivo gigante e inmanejable)

Con Blueprint:
    home_bp     → maneja "/"           (en home.py)
    producto_bp → maneja "/producto"   (en producto.py)
    empresa_bp  → maneja "/empresa"    (en empresa.py)
    (cada archivo maneja sus propias rutas, ordenado y limpio)

Es como organizar un libro en CAPÍTULOS en vez de tener todo
en una sola página interminable.
────────────────────────────────────────────────────────────────
"""

from flask import Blueprint, render_template
# Blueprint:       para crear un grupo de rutas.
# render_template: para convertir un archivo .html en una página web.
#                  Flask busca los archivos en la carpeta templates/.


# ─── Crear el Blueprint ──────────────────────────────────────
home_bp = Blueprint(
    "home",       # Nombre interno del Blueprint (para url_for)
    __name__      # Módulo actual (Flask lo usa para encontrar archivos)
)
# Después de esta línea, "home_bp" es un objeto Blueprint.
# Podemos usarlo con @home_bp.route() para definir rutas.


# ─── Ruta: Página de inicio ──────────────────────────────────
@home_bp.route("/")
def index():
    """
    Maneja la URL raíz: http://localhost:5100/

    ¿Qué hace @home_bp.route("/")?
    Es un "decorador". Le dice a Flask:
    "Cuando alguien visite la URL '/', ejecuta la función index()".

    La función retorna render_template("pages/home.html"),
    que busca el archivo templates/pages/home.html,
    lo procesa (reemplaza variables, ejecuta lógica Jinja2)
    y lo envía al navegador como HTML.
    """
    return render_template("pages/home.html")
    # Flask busca: templates/pages/home.html
    # Lo convierte en HTML puro y lo envía al navegador.
