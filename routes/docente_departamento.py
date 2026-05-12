from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.api_service import ApiService

docente_dept_bp = Blueprint('docente_departamento', __name__)
api = ApiService()
TABLA = 'docente_departamento'

@docente_dept_bp.route('/docente_departamento')
def index():
    accion = request.args.get('accion')
    docente_id = request.args.get('docente')
    depto_id = request.args.get('departamento')

    registros = api.listar(TABLA)
    programas = api.listar('programa')

    registro_editar = None
    if accion == 'editar' and docente_id and depto_id:
        # PK compuesta: usamos el método compuesto del ApiService
        registro_editar = api.get(f"{TABLA}/{docente_id}", depto_id)

    return render_template('pages/docente_departamento.html',
                           registros=registros,
                           programas=programas,
                           accion=accion,
                           registro_editar=registro_editar)

@docente_dept_bp.route('/docente_departamento/crear', methods=['POST'])
def crear():
    datos = {
        "docente":       int(request.form.get('docente')),
        "departamento":  int(request.form.get('departamento')),
        "dedicacion":    request.form.get('dedicacion'),
        "modalidad":     request.form.get('modalidad'),
        "fecha_ingreso": request.form.get('fecha_ingreso'),
        "fecha_salida":  request.form.get('fecha_salida') or None
    }
    exito, mensaje = api.crear(TABLA, datos)
    flash(mensaje, 'success' if exito else 'danger')
    return redirect(url_for('docente_departamento.index'))

@docente_dept_bp.route('/docente_departamento/actualizar', methods=['POST'])
def actualizar():
    docente_id = request.form.get('docente')
    depto_id = request.form.get('departamento')
    datos = {
        "dedicacion":    request.form.get('dedicacion'),
        "modalidad":     request.form.get('modalidad'),
        "fecha_ingreso": request.form.get('fecha_ingreso'),
        "fecha_salida":  request.form.get('fecha_salida') or None
    }
    # PK compuesta: usamos actualizar_compuesto del ApiService
    exito, mensaje = api.actualizar_compuesto(TABLA, docente_id, depto_id, datos)
    flash(mensaje, 'success' if exito else 'danger')
    return redirect(url_for('docente_departamento.index'))

@docente_dept_bp.route('/docente_departamento/eliminar', methods=['POST'])
def eliminar():
    docente_id = request.form.get('docente')
    depto_id = request.form.get('departamento')
    exito, mensaje = api.eliminar_compuesto(TABLA, docente_id, depto_id)
    flash(mensaje, 'success' if exito else 'danger')
    return redirect(url_for('docente_departamento.index'))