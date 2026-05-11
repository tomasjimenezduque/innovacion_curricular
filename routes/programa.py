from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.api_service import ApiService

programa_bp = Blueprint('programa', __name__)
api = ApiService()
TABLA = 'programa'
CLAVE = 'id'

@programa_bp.route('/programa')
def index():
    accion = request.args.get('accion')
    id_p = request.args.get('id')

    programas = api.listar(TABLA)
    facultades = api.listar('facultad')

    programa_editar = None
    if accion == 'editar' and id_p:
        programa_editar = api.get(TABLA, id_p)

    return render_template('pages/programa.html',
                           programas=programas,
                           facultades=facultades,
                           accion=accion,
                           programa_editar=programa_editar)

@programa_bp.route('/programa/crear', methods=['POST'])
def crear():
    datos = {
        "nombre":              request.form.get('nombre'),
        "tipo":                request.form.get('tipo'),
        "nivel":               request.form.get('nivel'),
        "fecha_creacion":      request.form.get('fecha_creacion'),
        "numero_cohortes":     request.form.get('numero_cohortes'),
        "cant_graduados":      request.form.get('cant_graduados'),
        "fecha_actualizacion": request.form.get('fecha_actualizacion'),
        "ciudad":              request.form.get('ciudad'),
        "facultad":            int(request.form.get('facultad')),
        "fecha_cierre":        request.form.get('fecha_cierre') or None
    }
    exito, mensaje = api.crear(TABLA, datos)
    flash(mensaje, 'success' if exito else 'danger')
    return redirect(url_for('programa.index'))

@programa_bp.route('/programa/actualizar', methods=['POST'])
def actualizar():
    id_p = request.form.get('id')
    datos = {
        "nombre":              request.form.get('nombre'),
        "tipo":                request.form.get('tipo'),
        "nivel":               request.form.get('nivel'),
        "fecha_creacion":      request.form.get('fecha_creacion'),
        "numero_cohortes":     request.form.get('numero_cohortes'),
        "cant_graduados":      request.form.get('cant_graduados'),
        "fecha_actualizacion": request.form.get('fecha_actualizacion'),
        "ciudad":              request.form.get('ciudad'),
        "facultad":            int(request.form.get('facultad')),
        "fecha_cierre":        request.form.get('fecha_cierre') or None
    }
    exito, mensaje = api.actualizar(TABLA, CLAVE, id_p, datos)
    flash(mensaje, 'success' if exito else 'danger')
    return redirect(url_for('programa.index'))

@programa_bp.route('/programa/eliminar', methods=['POST'])
def eliminar():
    id_p = request.form.get('id')
    exito, mensaje = api.eliminar(TABLA, CLAVE, id_p)
    flash(mensaje, 'success' if exito else 'danger')
    return redirect(url_for('programa.index'))