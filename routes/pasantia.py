from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.api_service import ApiService

pasantia_bp = Blueprint('pasantia', __name__)
api = ApiService()
TABLA = 'pasantia'
CLAVE = 'id'

@pasantia_bp.route('/pasantia')
def index():
    accion = request.args.get('accion')
    id_p = request.args.get('id')

    pasantias = api.listar(TABLA)
    programas = api.listar('programa')

    pasantia_editar = None
    if accion == 'editar' and id_p:
        pasantia_editar = api.get(TABLA, id_p)

    return render_template('pages/pasantia.html',
                           pasantias=pasantias,
                           programas=programas,
                           accion=accion,
                           pasantia_editar=pasantia_editar)

@pasantia_bp.route('/pasantia/crear', methods=['POST'])
def crear():
    datos = {
        "nombre":      request.form.get('nombre'),
        "pais":        request.form.get('pais'),
        "empresa":     request.form.get('empresa'),
        "descripcion": request.form.get('descripcion'),
        "programa":    int(request.form.get('programa'))
    }
    exito, mensaje = api.crear(TABLA, datos)
    flash(mensaje, 'success' if exito else 'danger')
    return redirect(url_for('pasantia.index'))

@pasantia_bp.route('/pasantia/actualizar', methods=['POST'])
def actualizar():
    id_p = request.form.get('id')
    datos = {
        "nombre":      request.form.get('nombre'),
        "pais":        request.form.get('pais'),
        "empresa":     request.form.get('empresa'),
        "descripcion": request.form.get('descripcion'),
        "programa":    int(request.form.get('programa'))
    }
    exito, mensaje = api.actualizar(TABLA, CLAVE, id_p, datos)
    flash(mensaje, 'success' if exito else 'danger')
    return redirect(url_for('pasantia.index'))

@pasantia_bp.route('/pasantia/eliminar', methods=['POST'])
def eliminar():
    id_p = request.form.get('id')
    exito, mensaje = api.eliminar(TABLA, CLAVE, id_p)
    flash(mensaje, 'success' if exito else 'danger')
    return redirect(url_for('pasantia.index'))