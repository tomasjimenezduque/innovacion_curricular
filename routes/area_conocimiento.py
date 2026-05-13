from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.api_service import ApiService

area_con_bp = Blueprint('area_conocimiento', __name__)
api = ApiService()
TABLA = 'area_conocimiento'
CLAVE = 'id'

@area_con_bp.route('/area_conocimiento')
def index():
    accion = request.args.get('accion')
    id_a = request.args.get('id')

    areas = api.listar(TABLA)

    area_editar = None
    if accion == 'editar' and id_a:
        area_editar = api.get(TABLA, id_a)

    return render_template('pages/area_conocimiento.html',
                           areas=areas,
                           accion=accion,
                           area_editar=area_editar)

@area_con_bp.route('/area_conocimiento/crear', methods=['POST'])
def crear():
    datos = {
        "gran_area":  request.form.get('gran_area'),
        "area":       request.form.get('area'),
        "disciplina": request.form.get('disciplina')
    }
    exito, mensaje = api.crear(TABLA, datos)
    flash(mensaje, 'success' if exito else 'danger')
    return redirect(url_for('area_conocimiento.index'))

@area_con_bp.route('/area_conocimiento/actualizar', methods=['POST'])
def actualizar():
    id_a = request.form.get('id')
    datos = {
        "gran_area":  request.form.get('gran_area'),
        "area":       request.form.get('area'),
        "disciplina": request.form.get('disciplina')
    }
    exito, mensaje = api.actualizar(TABLA, CLAVE, id_a, datos)
    flash(mensaje, 'success' if exito else 'danger')
    return redirect(url_for('area_conocimiento.index'))

@area_con_bp.route('/area_conocimiento/eliminar', methods=['POST'])
def eliminar():
    id_a = request.form.get('id')
    exito, mensaje = api.eliminar(TABLA, CLAVE, id_a)
    flash(mensaje, 'success' if exito else 'danger')
    return redirect(url_for('area_conocimiento.index'))