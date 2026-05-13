from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.api_service import ApiService

premio_bp = Blueprint('premio', __name__)
api = ApiService()
TABLA = 'premio'
CLAVE = 'id'

@premio_bp.route('/premio')
def index():
    accion = request.args.get('accion')
    id_p = request.args.get('id')

    premios = api.listar(TABLA)
    programas = api.listar('programa')

    premio_editar = None
    if accion == 'editar' and id_p:
        premio_editar = api.get(TABLA, id_p)

    return render_template('pages/premio.html',
                           premios=premios,
                           programas=programas,
                           accion=accion,
                           premio_editar=premio_editar)

@premio_bp.route('/premio/crear', methods=['POST'])
def crear():
    datos = {
        "nombre":            request.form.get('nombre'),
        "descripcion":       request.form.get('descripcion'),
        "fecha":             request.form.get('fecha'),
        "entidad_otorgante": request.form.get('entidad_otorgante'),
        "pais":              request.form.get('pais'),
        "programa":          int(request.form.get('programa'))
    }
    exito, mensaje = api.crear(TABLA, datos)
    flash(mensaje, 'success' if exito else 'danger')
    return redirect(url_for('premio.index'))

@premio_bp.route('/premio/actualizar', methods=['POST'])
def actualizar():
    id_p = request.form.get('id')
    datos = {
        "nombre":            request.form.get('nombre'),
        "descripcion":       request.form.get('descripcion'),
        "fecha":             request.form.get('fecha'),
        "entidad_otorgante": request.form.get('entidad_otorgante'),
        "pais":              request.form.get('pais'),
        "programa":          int(request.form.get('programa'))
    }
    exito, mensaje = api.actualizar(TABLA, CLAVE, id_p, datos)
    flash(mensaje, 'success' if exito else 'danger')
    return redirect(url_for('premio.index'))

@premio_bp.route('/premio/eliminar', methods=['POST'])
def eliminar():
    id_p = request.form.get('id')
    exito, mensaje = api.eliminar(TABLA, CLAVE, id_p)
    flash(mensaje, 'success' if exito else 'danger')
    return redirect(url_for('premio.index'))