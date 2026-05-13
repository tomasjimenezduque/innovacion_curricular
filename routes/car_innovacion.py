from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.api_service import ApiService

car_innovacion_bp = Blueprint('car_innovacion', __name__)
api = ApiService()
TABLA = 'car_innovacion'
CLAVE = 'id'

@car_innovacion_bp.route('/car_innovacion')
def index():
    accion = request.args.get('accion')
    id_c = request.args.get('id')

    innovaciones = api.listar(TABLA)

    innovacion_editar = None
    if accion == 'editar' and id_c:
        innovacion_editar = api.get(TABLA, id_c)

    return render_template('pages/car_innovacion.html',
                           innovaciones=innovaciones,
                           accion=accion,
                           innovacion_editar=innovacion_editar)

@car_innovacion_bp.route('/car_innovacion/crear', methods=['POST'])
def crear():
    datos = {
        "nombre":      request.form.get('nombre'),
        "descripcion": request.form.get('descripcion'),
        "tipo":        request.form.get('tipo')
    }
    exito, mensaje = api.crear(TABLA, datos)
    flash(mensaje, 'success' if exito else 'danger')
    return redirect(url_for('car_innovacion.index'))

@car_innovacion_bp.route('/car_innovacion/actualizar', methods=['POST'])
def actualizar():
    id_c = request.form.get('id')
    datos = {
        "nombre":      request.form.get('nombre'),
        "descripcion": request.form.get('descripcion'),
        "tipo":        request.form.get('tipo')
    }
    exito, mensaje = api.actualizar(TABLA, CLAVE, id_c, datos)
    flash(mensaje, 'success' if exito else 'danger')
    return redirect(url_for('car_innovacion.index'))

@car_innovacion_bp.route('/car_innovacion/eliminar', methods=['POST'])
def eliminar():
    id_c = request.form.get('id')
    exito, mensaje = api.eliminar(TABLA, CLAVE, id_c)
    flash(mensaje, 'success' if exito else 'danger')
    return redirect(url_for('car_innovacion.index'))