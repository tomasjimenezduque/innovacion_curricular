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
        universidad_editar = api.get("universidad", id_u)

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
    # Debemos capturar los nombres EXACTOS que el HTML envía 
    # y que el Modelo de SQLAlchemy espera.
    datos = {
        "id": request.form.get("id"),
        "nombre": request.form.get("nombre"),
        "ciudad": request.form.get("ciudad"),  # CAMBIADO: Antes decía 'ubicacion'
        "tipo": request.form.get("tipo")       # AGREGADO: Para que no vaya vacío
    }
    
    exito, mensaje = api.crear("universidad", datos)
    flash(mensaje, "success" if exito else "danger")
    return redirect(url_for("universidad.index"))

# ═══════════════════════════════════════════════════════════════
#  ACTUALIZAR — Enviar cambios a la API
# ═══════════════════════════════════════════════════════════════
# universidad_routes.py (en el proyecto FRONT/FLASK)

@universidad_bp.route('/actualizar', methods=['POST'])
def actualizar():
    # 1. Capturamos los datos del formulario
    id_u = request.form.get('id')
    datos = {
        "nombre": request.form.get('nombre'),
        "ciudad": request.form.get('ciudad'),
        "tipo": request.form.get('tipo')
    }
    
    # 2. Llamamos al ApiService (el que me mostraste antes)
    # Importante: Pasar 'valor_clave' como el ID
    exito, mensaje = api.actualizar(
        tabla="universidad", 
        clave_nombre="id", 
        valor_clave=id_u, 
        datos=datos
    )
    
    if exito:
        flash("Universidad actualizada correctamente", "success")
    else:
        flash(f"Error al actualizar: {mensaje}", "danger")
        
    return redirect(url_for('universidad.index'))

@universidad_bp.route('/eliminar', methods=['POST'])
def eliminar():
    id_u = request.form.get('id')
    
    # Llamamos al ApiService
    exito, mensaje = api.eliminar(
        tabla="universidad", 
        clave_nombre="id", 
        valor_clave=id_u
    )
    
    if exito:
        flash("Registro eliminado con éxito", "success")
    else:
        flash(f"Error al eliminar: {mensaje}", "danger")
        
    return redirect(url_for('universidad.index'))