from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.api_service import ApiService
from datetime import datetime

usuario_bp = Blueprint('usuario', __name__)
api = ApiService()

# Constantes para mantener la consistencia
TABLA = 'usuario'
CLAVE = 'id' 

# ═══════════════════════════════════════════════════════════════
#  RUTA PRINCIPAL — Listar y gestionar estados de la vista
# ═══════════════════════════════════════════════════════════════
@usuario_bp.route('/usuario')
def index():
    limite = request.args.get('limite', type=int)
    accion = request.args.get('accion', '')
    valor_id = request.args.get('id', '')

    registros = api.listar(TABLA, limite)
    
    # Caso: Abrir formulario de creación
    if accion == 'nuevo':
        roles = api.listar('rol') # Necesario para el select en crear_usuario.html
        hoy = datetime.now().strftime('%Y-%m-%d')
        return render_template('pages/crear_usuario.html', roles=roles, fecha_actual=hoy)

    # Caso: Cargar datos para edición
    registro = None
    if accion == 'editar' and valor_id:
        # Usamos .get() que es el método existente en tu ApiService
        registro = api.get(TABLA, valor_id)

    return render_template(
        'pages/usuario.html',
        registros=registros, 
        mostrar_formulario=(accion == 'editar'),
        editando=(accion == 'editar'), 
        registro=registro, 
        limite=limite
    )

# ═══════════════════════════════════════════════════════════════
#  CREAR — Sincronizado con las columnas de PostgreSQL
# ═══════════════════════════════════════════════════════════════
@usuario_bp.route('/usuario/crear', methods=['POST'])
def crear():
    rol_raw = request.form.get('rol_id')
    
    if not rol_raw:
        flash("Error: El campo Rol es obligatorio.", "danger")
        return redirect(url_for('usuario.index', accion='nuevo'))

    # Mapeo exacto según el log de SQLAlchemy:
    # username, password, email, nombre_completo, activo, id_rol
    datos = {
        'username':        request.form.get('username'),
        'email':           request.form.get('email'),
        'password':        request.form.get('password'),
        'nombre_completo': request.form.get('nombre_completo'),
        'id_rol':          int(rol_raw), # Se envía id_rol, no 'id'
        'activo':          'activo' in request.form,
    }
    
    exito, mensaje = api.crear(TABLA, datos)
    
    flash(mensaje, 'success' if exito else 'danger')
    return redirect(url_for('usuario.index'))

# ═══════════════════════════════════════════════════════════════
#  ACTUALIZAR — Integración con ApiService
# ═══════════════════════════════════════════════════════════════
@usuario_bp.route('/usuario/actualizar', methods=['POST'])
def actualizar():
    id_u = request.form.get('id')
    rol_raw = request.form.get('rol_id')

    if not id_u:
        flash("ID de usuario no proporcionado", "danger")
        return redirect(url_for('usuario.index'))

    datos = {
        'username':        request.form.get('username'),
        'email':           request.form.get('email'),
        'nombre_completo': request.form.get('nombre_completo'),
        'id_rol':          int(rol_raw) if rol_raw else None,
        'activo':          'activo' in request.form,
    }

    # Se incluye clave_nombre="id" para evitar el TypeError
    exito, mensaje = api.actualizar(
        tabla=TABLA,
        clave_nombre=CLAVE,
        valor_id=id_u,
        datos=datos
    )

    flash(mensaje, 'success' if exito else 'danger')
    return redirect(url_for('usuario.index'))

# ═══════════════════════════════════════════════════════════════
#  ELIMINAR — Corrección del BuildError
# ═══════════════════════════════════════════════════════════════
@usuario_bp.route('/usuario/eliminar', methods=['POST'])
def eliminar():
    id_u = request.form.get('id')
    
    if not id_u:
        flash("Error: ID no encontrado", "danger")
        return redirect(url_for('usuario.index'))

    # Pasas: recurso, nombre_clave, valor_id
    # Nota: Los pasamos de forma posicional para evitar líos de nombres
    exito, mensaje = api.eliminar("usuario", id_u, "id") 
    
    flash(mensaje, 'success' if exito else 'danger')
    return redirect(url_for('usuario.index'))