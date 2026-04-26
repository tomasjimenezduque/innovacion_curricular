from flask import Blueprint, render_template, request, redirect, url_for, flash
from services import ApiService

# ─── Crear el Blueprint para Universidad ───────────────────
universidad_bp = Blueprint("universidad", __name__)
api = ApiService()

# ═══════════════════════════════════════════════════════════════
#  RUTA PRINCIPAL — Listar + mostrar formularios
# ═══════════════════════════════════════════════════════════════
@universidad_bp.route("/universidad")
def index():
    """
    Muestra la lista de universidades y los formularios de CRUD.
    """
    limite = request.args.get("limite")
    accion = request.args.get("accion") # "nuevo", "editar" o None
    id_u = request.args.get("id")       # Usamos 'id' como clave para universidad

    # Consultamos al Backend (FastAPI) a través del ApiService
    universidades = api.listar("universidad", limite=limite)

    universidad_editar = None
    if accion == "editar" and id_u:
        universidad_editar = api.obtener("universidad", id_u)

    return render_template(
        "pages/universidad.html",
        universidades=universidades,
        accion=accion,
        universidad_editar=universidad_editar,
        limite=limite
    )

# ═══════════════════════════════════════════════════════════════
#  CREAR — Recibir formulario y enviar a la API
# ═══════════════════════════════════════════════════════════════
@universidad_bp.route("/universidad/crear", methods=["POST"])
def crear():
    datos = {
        "nombre": request.form.get("nombre"),
        "ubicacion": request.form.get("ubicacion"), # Ejemplo de campo adicional
        # Agrega aquí más campos según tu modelo de base de datos
    }
    
    exito, mensaje = api.crear("universidad", datos)
    flash(mensaje, "success" if exito else "danger")
    return redirect(url_for("universidad.index"))

# ═══════════════════════════════════════════════════════════════
#  ACTUALIZAR — Enviar cambios a la API
# ═══════════════════════════════════════════════════════════════
@universidad_bp.route("/universidad/actualizar", methods=["POST"])
def actualizar():
    id_u = request.form.get("id")
    datos = {
        "nombre": request.form.get("nombre"),
        "ubicacion": request.form.get("ubicacion"),
    }
    
    exito, mensaje = api.actualizar("universidad", id_u, datos)
    flash(mensaje, "success" if exito else "danger")
    return redirect(url_for("universidad.index"))

# ═══════════════════════════════════════════════════════════════
#  ELIMINAR — Borrar registro en la API
# ═══════════════════════════════════════════════════════════════
@universidad_bp.route("/universidad/eliminar", methods=["POST"])
def eliminar():
    id_u = request.form.get("id")
    
    exito, mensaje = api.eliminar("universidad", id_u)
    flash(mensaje, "success" if exito else "danger")
    return redirect(url_for("universidad.index"))