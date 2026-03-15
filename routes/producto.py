"""
producto.py — Rutas para el CRUD completo de Productos.

Este archivo maneja 4 URLs:
──────────────────────────────────────────────────────────────
│ URL                   │ Método │ ¿Qué hace?              │
──────────────────────────────────────────────────────────────
│ /producto             │ GET    │ Listar + mostrar forms   │
│ /producto/crear       │ POST   │ Crear nuevo producto     │
│ /producto/actualizar  │ POST   │ Actualizar producto      │
│ /producto/eliminar    │ POST   │ Eliminar producto        │
──────────────────────────────────────────────────────────────

NOTA: Crear, Actualizar y Eliminar usan POST (no PUT/DELETE).
¿Por qué? Los formularios HTML solo soportan GET y POST.
El método real (POST/PUT/DELETE) lo maneja ApiService internamente.

────────────────────────────────────────────────────────────────
FLUJO DE DATOS (Ejemplo: Crear Producto)
────────────────────────────────────────────────────────────────
1. Usuario llena el formulario en el navegador y da clic en "Guardar"
2. El navegador envía un POST a /producto/crear con los datos del form
3. Flask ejecuta la función crear() de este archivo
4. crear() extrae los datos del formulario (request.form)
5. crear() llama a api.crear("producto", datos)
6. ApiService envía un POST HTTP a la API FastAPI
7. FastAPI guarda en PostgreSQL y responde JSON
8. ApiService retorna (True/False, mensaje)
9. crear() guarda el mensaje con flash() y redirige a /producto
10. El navegador muestra la lista actualizada con el mensaje
────────────────────────────────────────────────────────────────
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash
# Blueprint:       para crear grupo de rutas (ya lo conocemos)
# render_template: para renderizar HTML (ya lo conocemos)
# request:         para acceder a los datos del formulario (request.form)
#                  y a los parámetros de la URL (request.args)
# redirect:        para redirigir al usuario a otra URL
#                  (ej: después de crear, redirigir a la lista)
# url_for:         para generar URLs a partir del nombre de la función
#                  (ej: url_for("producto.index") → "/producto")
# flash:           para guardar un mensaje que se muestra UNA sola vez
#                  en la siguiente página (mensajes de éxito/error)

from services import ApiService
# Importa nuestra clase ApiService para comunicarnos con la API.


# ─── Crear el Blueprint ──────────────────────────────────────
producto_bp = Blueprint(
    "producto",     # Nombre interno. Se usa en url_for("producto.index")
    __name__        # Módulo actual
)

# ─── Crear instancia del servicio API ─────────────────────────
api = ApiService()
# Creamos UNA sola instancia que reutilizaremos en todas las funciones.
# No necesitamos crear una nueva en cada función porque ApiService
# no guarda estado (no tiene datos que cambien entre llamadas).


# ═══════════════════════════════════════════════════════════════
#  RUTA PRINCIPAL — Listar productos + mostrar formularios
# ═══════════════════════════════════════════════════════════════
@producto_bp.route("/producto")
def index():
    """
    Página principal de productos: http://localhost:5100/producto

    Esta función maneja TRES situaciones con la MISMA URL,
    usando parámetros de consulta (?accion=...):

    1. Solo listar → /producto
       Muestra la tabla con todos los productos.

    2. Crear nuevo → /producto?accion=nuevo
       Muestra la tabla + formulario vacío para crear.

    3. Editar existente → /producto?accion=editar&clave=PR001
       Muestra la tabla + formulario con datos del producto PR001.

    ¿Qué son los "parámetros de consulta" (query params)?
    ─────────────────────────────────────────────────────
    Son valores que van después del "?" en la URL.
    Ejemplo: /producto?limite=5&accion=nuevo
        - limite = 5
        - accion = "nuevo"
    Se acceden con: request.args.get("nombre_parametro")
    """

    # ─── Leer parámetros de la URL ───────────────────────────
    limite = request.args.get("limite")
    # Obtiene el valor de "limite" de la URL.
    # Si la URL es /producto?limite=5 → limite = "5"
    # Si no hay parámetro limite      → limite = None

    accion = request.args.get("accion")
    # "accion" indica si el usuario quiere crear o editar.
    # Valores posibles: "nuevo", "editar", o None (solo listar)

    clave = request.args.get("clave")
    # "clave" es el código del producto a editar.
    # Solo tiene valor cuando accion = "editar"
    # Ejemplo: clave = "PR001"

    # ─── Obtener lista de productos de la API ─────────────────
    productos = api.listar("producto", limite=limite)
    # Llama a la API: GET http://localhost:8000/api/producto/?limite=X
    # Retorna una lista de diccionarios:
    # [{"codigo": "PR001", "nombre": "Laptop", "stock": 17, ...}, ...]

    # ─── Si estamos editando, obtener datos del producto ──────
    producto_editar = None
    # Inicializamos en None. Solo tendrá datos si accion == "editar".

    if accion == "editar" and clave:
        producto_editar = api.obtener("producto", clave)
        # Llama a la API: GET http://localhost:8000/api/producto/PR001
        # Retorna un diccionario: {"codigo": "PR001", "nombre": "Laptop", ...}
        # O None si no existe.

    # ─── Renderizar la plantilla HTML ─────────────────────────
    return render_template(
        "pages/producto.html",      # Archivo HTML a renderizar
        productos=productos,         # Lista de productos (para la tabla)
        accion=accion,               # "nuevo", "editar", o None
        producto_editar=producto_editar,  # Datos del producto a editar (o None)
        limite=limite                # Límite actual (para mantenerlo en el form)
    )
    # render_template pasa estas variables a la plantilla HTML.
    # Dentro del HTML, se acceden como: {{ productos }}, {{ accion }}, etc.


# ═══════════════════════════════════════════════════════════════
#  CREAR — Recibir formulario y crear producto en la API
# ═══════════════════════════════════════════════════════════════
@producto_bp.route("/producto/crear", methods=["POST"])
def crear():
    """
    Recibe los datos del formulario de creación y los envía a la API.

    methods=["POST"] significa que esta ruta SOLO acepta peticiones POST.
    Las peticiones GET a /producto/crear darán error 405 (Method Not Allowed).

    ¿Por qué solo POST?
    Porque esta ruta recibe datos del formulario. Los formularios HTML
    envían datos con POST (en el cuerpo de la petición, no en la URL).
    """

    # ─── Extraer datos del formulario ─────────────────────────
    # request.form es un diccionario con los datos del formulario HTML.
    # Cada campo del formulario tiene un atributo "name" en HTML:
    #   <input name="codigo"> → request.form.get("codigo")
    datos = {
        "codigo":        request.form.get("codigo"),
        "nombre":        request.form.get("nombre"),
        "stock":         int(request.form.get("stock", 0)),
        "valorunitario": float(request.form.get("valorunitario", 0))
    }
    # "stock" y "valorunitario" vienen como texto desde el formulario
    # (todo en HTML es texto). Los convertimos a int y float.
    # int("17") → 17
    # float("2500000.0") → 2500000.0
    #
    # request.form.get("stock", 0): si "stock" no existe, usa 0 como default.
    # Esto evita errores si el campo está vacío.

    # ─── Enviar a la API ──────────────────────────────────────
    exito, mensaje = api.crear("producto", datos)
    # api.crear() retorna una TUPLA: (True/False, "mensaje")
    # Usamos "desempaquetado de tupla" para separar los dos valores:
    #   exito   = True o False
    #   mensaje = "Producto creado exitosamente." o "Error: ..."

    # ─── Mostrar mensaje al usuario ───────────────────────────
    if exito:
        flash(mensaje, "success")
        # flash() guarda un mensaje en la sesión del usuario.
        # "success" es la categoría (se usa para el color del alert).
        # El mensaje se mostrará UNA sola vez en la siguiente página.
    else:
        flash(mensaje, "danger")
        # "danger" = color rojo (error) en Bootstrap.

    # ─── Redirigir a la lista de productos ────────────────────
    return redirect(url_for("producto.index"))
    # redirect() envía al navegador a otra URL.
    # url_for("producto.index") genera la URL "/producto"
    #   - "producto" = nombre del Blueprint
    #   - "index"    = nombre de la función
    #
    # ¿Por qué redirigir en vez de mostrar directamente?
    # Es el patrón POST-Redirect-GET (PRG):
    #   1. POST: el usuario envía el formulario
    #   2. Redirect: el servidor redirige a una URL GET
    #   3. GET: el navegador carga la nueva página
    # Si no redirigimos, al refrescar la página se re-enviaría
    # el formulario (creando otro producto duplicado).


# ═══════════════════════════════════════════════════════════════
#  ACTUALIZAR — Recibir formulario y actualizar producto
# ═══════════════════════════════════════════════════════════════
@producto_bp.route("/producto/actualizar", methods=["POST"])
def actualizar():
    """
    Recibe los datos del formulario de edición y actualiza en la API.

    Es muy similar a crear(), pero usa api.actualizar() (PUT)
    en vez de api.crear() (POST).
    """

    # ─── Extraer datos del formulario ─────────────────────────
    codigo = request.form.get("codigo")
    # El código es la clave primaria. Lo necesitamos para decirle
    # a la API CUÁL producto actualizar.

    datos = {
        "codigo":        codigo,
        "nombre":        request.form.get("nombre"),
        "stock":         int(request.form.get("stock", 0)),
        "valorunitario": float(request.form.get("valorunitario", 0))
    }

    # ─── Enviar a la API ──────────────────────────────────────
    exito, mensaje = api.actualizar("producto", codigo, datos)
    # api.actualizar() usa PUT en vez de POST.
    # El "codigo" va en la URL: PUT /api/producto/PR001
    # Los "datos" van en el cuerpo JSON.

    # ─── Mostrar mensaje y redirigir ──────────────────────────
    flash(mensaje, "success" if exito else "danger")
    # Versión corta del if/else. Es equivalente a:
    # if exito:
    #     categoria = "success"
    # else:
    #     categoria = "danger"
    # flash(mensaje, categoria)

    return redirect(url_for("producto.index"))


# ═══════════════════════════════════════════════════════════════
#  ELIMINAR — Recibir confirmación y eliminar producto
# ═══════════════════════════════════════════════════════════════
@producto_bp.route("/producto/eliminar", methods=["POST"])
def eliminar():
    """
    Recibe la confirmación de eliminación y borra el producto en la API.

    El formulario solo envía el código del producto a eliminar.
    La confirmación se hace con JavaScript (confirm()) ANTES
    de enviar el formulario.
    """

    # ─── Extraer el código del producto a eliminar ────────────
    codigo = request.form.get("codigo")

    # ─── Enviar a la API ──────────────────────────────────────
    exito, mensaje = api.eliminar("producto", codigo)
    # api.eliminar() usa DELETE: DELETE /api/producto/PR001

    # ─── Mostrar mensaje y redirigir ──────────────────────────
    flash(mensaje, "success" if exito else "danger")
    return redirect(url_for("producto.index"))
