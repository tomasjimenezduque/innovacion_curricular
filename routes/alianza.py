from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.api_service import ApiService

alianza_bp = Blueprint('alianza', __name__)
api = ApiService()
TABLA = 'alianza'

@alianza_bp.route('/alianza')
def index():
    accion = request.args.get('accion')
    aliado_nit = request.args.get('aliado')
    depto_id = request.args.get('departamento')

    alianzas = api.listar(TABLA)
    aliados = api.listar('aliado')
    programas = api.listar('programa')

    registro_editar = None
    if accion == 'editar' and aliado_nit and depto_id:
        registro_editar = api.get(f"{TABLA}/{aliado_nit}", depto_id)

    return render_template('pages/alianza.html',
                           alianzas=alianzas,
                           aliados=aliados,
                           programas=programas,
                           accion=accion,
                           registro_editar=registro_editar)

@alianza_bp.route('/alianza/crear', methods=['POST'])
def crear():
    datos = {
        "aliado":       request.form.get('aliado'),  # string NIT
        "departamento": int(request.form.get('departamento')),
        "fecha_inicio": request.form.get('fecha_inicio'),
        "fecha_fin":    request.form.get('fecha_fin') or None,
        "docente":      int(request.form.get('docente')) if request.form.get('docente') else None
    }
    exito, mensaje = api.crear(TABLA, datos)
    flash(mensaje, 'success' if exito else 'danger')
    return redirect(url_for('alianza.index'))

@alianza_bp.route('/alianza/actualizar', methods=['POST'])
def actualizar():
    aliado_nit = request.form.get('aliado')
    depto_id = request.form.get('departamento')
    datos = {
        "fecha_inicio": request.form.get('fecha_inicio'),
        "fecha_fin":    request.form.get('fecha_fin') or None,
        "docente":      int(request.form.get('docente')) if request.form.get('docente') else None
    }
    exito, mensaje = api.actualizar_compuesto(TABLA, aliado_nit, depto_id, datos)
    flash(mensaje, 'success' if exito else 'danger')
    return redirect(url_for('alianza.index'))

@alianza_bp.route('/alianza/eliminar', methods=['POST'])
def eliminar():
    aliado_nit = request.form.get('aliado')
    depto_id = request.form.get('departamento')
    exito, mensaje = api.eliminar_compuesto(TABLA, aliado_nit, depto_id)
    flash(mensaje, 'success' if exito else 'danger')
    return redirect(url_for('alianza.index'))