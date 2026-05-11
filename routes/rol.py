from flask import Blueprint, render_template, request, redirect, url_for, flash
from services import ApiService  # <--- Importación idéntica a Universidad

# ─── Crear el Blueprint para Rol ───────────────────────────
rol_bp = Blueprint("rol", __name__)
api = ApiService() # <--- Instancia de la clase

# ═══════════════════════════════════════════════════════════════
#  RUTA PRINCIPAL — Listar + mostrar formularios
# ═══════════════════════════════════════════════════════════════
@rol_bp.route("/rol")
def index():
    limite = request.args.get("limite")
    accion = request.args.get("accion") # "nuevo", "editar" o None
    id_r = request.args.get("id")

    roles = api.listar("rol", limite=limite)

    rol_editar = None
    if accion == "editar" and id_r:
        rol_editar = api.get("rol", id_r)

    return render_template(
        "pages/rol.html",
        roles=roles,
        accion=accion,
        rol_editar=rol_editar,
        limite=limite
    )

# ═══════════════════════════════════════════════════════════════
#  CREAR — Recibir formulario y enviar a la API
# ═══════════════════════════════════════════════════════════════
@rol_bp.route("/rol/crear", methods=["POST"])
def crear():
    datos = {
        "nombre": request.form.get("nombre"),
        "descripcion": request.form.get("descripcion"),
        "activo": 'activo' in request.form  # Maneja el checkbox
    }
    
    exito, mensaje = api.crear("rol", datos)
    flash(mensaje, "success" if exito else "danger")
    return redirect(url_for("rol.index"))

# ═══════════════════════════════════════════════════════════════
#  ACTUALIZAR — Enviar cambios a la API
# ═══════════════════════════════════════════════════════════════
@rol_bp.route('/rol/actualizar', methods=['POST'])
def actualizar():
    id_r = request.form.get('id')
    datos = {
        "nombre": request.form.get('nombre'),
        "descripcion": request.form.get('descripcion'),
        "activo": 'activo' in request.form
    }
    
    exito, mensaje = api.actualizar(
        tabla="rol", 
        clave_nombre="id", 
        valor_clave=id_r, 
        datos=datos
    )
    
    if exito:
        flash("Rol actualizado correctamente", "success")
    else:
        flash(f"Error al actualizar: {mensaje}", "danger")
        
    return redirect(url_for('rol.index'))

# ═══════════════════════════════════════════════════════════════
#  ELIMINAR
# ═══════════════════════════════════════════════════════════════
@rol_bp.route('/rol/eliminar', methods=['POST'])
def eliminar():
    id_r = request.form.get('id')
    
    exito, mensaje = api.eliminar(
        tabla="rol", 
        clave_nombre="id", 
        valor_clave=id_r
    )
    
    if exito:
        flash("Rol eliminado con éxito", "success")
    else:
        flash(f"Error al eliminar: {mensaje}", "danger")
        
    return redirect(url_for('rol.index'))