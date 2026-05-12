from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.api_service import ApiService

activ_academica_bp = Blueprint('activ_academica', __name__)
api = ApiService()
TABLA = 'activ_academica'
CLAVE = 'id'

@activ_academica_bp.route('/activ_academica')
def index():
    accion = request.args.get('accion')
    id_a = request.args.get('id')

    actividades = api.listar(TABLA)
    programas = api.listar('programa')

    actividad_editar = None
    if accion == 'editar' and id_a:
        actividad_editar = api.get(TABLA, id_a)

    return render_template('pages/activ_academica.html',
                           actividades=actividades,
                           programas=programas,
                           accion=accion,
                           actividad_editar=actividad_editar)

@activ_academica_bp.route('/activ_academica/crear', methods=['POST'])
def crear():
    datos = {
        "nombre":          request.form.get('nombre'),
        "num_creditos":    int(request.form.get('num_creditos')),
        "tipo":            request.form.get('tipo'),
        "area_formacion":  request.form.get('area_formacion'),
        "h_acom":          int(request.form.get('h_acom')),
        "h_indep":         int(request.form.get('h_indep')),
        "idioma":          request.form.get('idioma'),
        "espejo":          int(request.form.get('espejo')),
        "entidad_espejo":  request.form.get('entidad_espejo') or '',
        "pais_espejo":     request.form.get('pais_espejo') or '',
        "disenio":         int(request.form.get('disenio')) if request.form.get('disenio') else None
    }
    exito, mensaje = api.crear(TABLA, datos)
    flash(mensaje, 'success' if exito else 'danger')
    return redirect(url_for('activ_academica.index'))

@activ_academica_bp.route('/activ_academica/actualizar', methods=['POST'])
def actualizar():
    id_a = request.form.get('id')
    datos = {
        "nombre":          request.form.get('nombre'),
        "num_creditos":    int(request.form.get('num_creditos')),
        "tipo":            request.form.get('tipo'),
        "area_formacion":  request.form.get('area_formacion'),
        "h_acom":          int(request.form.get('h_acom')),
        "h_indep":         int(request.form.get('h_indep')),
        "idioma":          request.form.get('idioma'),
        "espejo":          int(request.form.get('espejo')),
        "entidad_espejo":  request.form.get('entidad_espejo') or '',
        "pais_espejo":     request.form.get('pais_espejo') or '',
        "disenio":         int(request.form.get('disenio')) if request.form.get('disenio') else None
    }
    exito, mensaje = api.actualizar(TABLA, CLAVE, id_a, datos)
    flash(mensaje, 'success' if exito else 'danger')
    return redirect(url_for('activ_academica.index'))

@activ_academica_bp.route('/activ_academica/eliminar', methods=['POST'])
def eliminar():
    id_a = request.form.get('id')
    exito, mensaje = api.eliminar(TABLA, CLAVE, id_a)
    flash(mensaje, 'success' if exito else 'danger')
    return redirect(url_for('activ_academica.index'))