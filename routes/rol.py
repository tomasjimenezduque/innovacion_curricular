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
    accion = request.args.get("accion") 
    id_r = request.args.get("id")

    roles = api.listar("rol", limite=limite)

    rol_editar = None
    if accion == "editar" and id_r:
        # Usamos el método 'get' que sí existe en tu ApiService
        # Según tu estructura, este método devuelve directamente el objeto o None
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
@rol_bp.route('/rol/crear', methods=['POST'])
def crear():
    # En Python/Flask, 'activo' in request.form devuelve True si se marcó, False si no.
    datos = {
        "nombre": request.form.get('nombre'),
        "descripcion": request.form.get('descripcion'),
        "activo": 'activo' in request.form  # Esto garantiza un booleano para SQL
    }
    
    # Llamada al ApiService (sin el parámetro de encriptación que causaba error)
    exito, mensaje = api.crear(tabla="rol", datos=datos)
    
    if exito:
        flash("Rol creado exitosamente", "success")
    else:
        flash(f"Error al crear: {mensaje}", "danger")
        
    return redirect(url_for('rol.index'))

# ═══════════════════════════════════════════════════════════════
#  ACTUALIZAR — Enviar cambios a la API
# ═══════════════════════════════════════════════════════════════
@rol_bp.route('/rol/actualizar', methods=['POST'])
def actualizar():
    # 1. Capturamos el ID del formulario
    id_r = request.form.get('id')
    
    # 2. Validamos que el ID exista antes de proceder
    if not id_r:
        flash("Error: No se proporcionó un ID válido para actualizar", "danger")
        return redirect(url_for('rol.index'))

    # 3. Preparamos el diccionario de datos
    datos = {
        "nombre": request.form.get('nombre'),
        "descripcion": request.form.get('descripcion'),
        "activo": 'activo' in request.form
    }
    
    # 4. Llamada al ApiService
    # NOTA: Asegúrate de que el orden sea (tabla, valor_id, datos)
    # o usa argumentos de palabra clave que coincidan con tu api_service.py
    exito, mensaje = api.actualizar(
        tabla="rol",
        clave_nombre="id", 
        valor_id=id_r,  # Cambiado de valor_clave a valor_id según el error previo
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
    
    if not id_r:
        flash("Error: ID no encontrado para eliminar", "danger")
        return redirect(url_for('rol.index'))

    # Usamos la firma consistente con actualizar: tabla y valor_id
    exito, mensaje = api.eliminar(
        tabla="rol", 
        valor_id=id_r
    )
    
    if exito:
        flash("Rol eliminado con éxito", "success")
    else:
        flash(f"Error al eliminar: {mensaje}", "danger")
        
    return redirect(url_for('rol.index'))