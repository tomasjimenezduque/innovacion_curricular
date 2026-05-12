from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.api_service import ApiService

enfoque_bp = Blueprint('enfoque', __name__)
api = ApiService()
TABLA = 'enfoque'
CLAVE = 'id'

@enfoque_bp.route('/enfoque')
def index():
    accion = request.args.get('accion')
    id_e = request.args.get('id')

    enfoques = api.listar(TABLA)

    enfoque_editar = None
    if accion == 'editar' and id_e:
        enfoque_editar = api.get(TABLA, id_e)

    return render_template('pages/enfoque.html',
                           enfoques=enfoques,
                           accion=accion,
                           enfoque_editar=enfoque_editar)

@enfoque_bp.route('/enfoque/crear', methods=['POST'])
def crear():
    datos = {
        "nombre":      request.form.get('nombre'),
        "descripcion": request.form.get('descripcion')
    }
    exito, mensaje = api.crear(TABLA, datos)
    flash(mensaje, 'success' if exito else 'danger')
    return redirect(url_for('enfoque.index'))

@enfoque_bp.route('/enfoque/actualizar', methods=['POST'])
def actualizar():
    id_e = request.form.get('id')
    datos = {
        "nombre":      request.form.get('nombre'),
        "descripcion": request.form.get('descripcion')
    }
    exito, mensaje = api.actualizar(TABLA, CLAVE, id_e, datos)
    flash(mensaje, 'success' if exito else 'danger')
    return redirect(url_for('enfoque.index'))

@enfoque_bp.route('/enfoque/eliminar', methods=['POST'])
def eliminar():
    id_e = request.form.get('id')
    exito, mensaje = api.eliminar(TABLA, CLAVE, id_e)
    flash(mensaje, 'success' if exito else 'danger')
    return redirect(url_for('enfoque.index'))