from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.api_service import ApiService

aspecto_normativo_bp = Blueprint('aspecto_normativo', __name__)
api = ApiService()
TABLA = 'aspecto_normativo'
CLAVE = 'id'

@aspecto_normativo_bp.route('/aspecto_normativo')
def index():
    accion = request.args.get('accion')
    id_a = request.args.get('id')

    aspectos = api.listar(TABLA)

    aspecto_editar = None
    if accion == 'editar' and id_a:
        aspecto_editar = api.get(TABLA, id_a)

    return render_template('pages/aspecto_normativo.html',
                           aspectos=aspectos,
                           accion=accion,
                           aspecto_editar=aspecto_editar)

@aspecto_normativo_bp.route('/aspecto_normativo/crear', methods=['POST'])
def crear():
    datos = {
        "tipo":        request.form.get('tipo'),
        "descripcion": request.form.get('descripcion'),
        "fuente":      request.form.get('fuente')
    }
    exito, mensaje = api.crear(TABLA, datos)
    flash(mensaje, 'success' if exito else 'danger')
    return redirect(url_for('aspecto_normativo.index'))

@aspecto_normativo_bp.route('/aspecto_normativo/actualizar', methods=['POST'])
def actualizar():
    id_a = request.form.get('id')
    datos = {
        "tipo":        request.form.get('tipo'),
        "descripcion": request.form.get('descripcion'),
        "fuente":      request.form.get('fuente')
    }
    exito, mensaje = api.actualizar(TABLA, CLAVE, id_a, datos)
    flash(mensaje, 'success' if exito else 'danger')
    return redirect(url_for('aspecto_normativo.index'))

@aspecto_normativo_bp.route('/aspecto_normativo/eliminar', methods=['POST'])
def eliminar():
    id_a = request.form.get('id')
    exito, mensaje = api.eliminar(TABLA, CLAVE, id_a)
    flash(mensaje, 'success' if exito else 'danger')
    return redirect(url_for('aspecto_normativo.index'))