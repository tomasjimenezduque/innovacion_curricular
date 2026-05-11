from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.api_service import ApiService

aliado_bp = Blueprint('aliado', __name__)
api = ApiService()
TABLA = 'aliado'
CLAVE = 'nit'

@aliado_bp.route('/aliado')
def index():
    accion = request.args.get('accion')
    nit = request.args.get('id')

    aliados = api.listar(TABLA)

    aliado_editar = None
    if accion == 'editar' and nit:
        aliado_editar = api.get(TABLA, nit)

    return render_template('pages/aliado.html',
                           aliados=aliados,
                           accion=accion,
                           aliado_editar=aliado_editar)

@aliado_bp.route('/aliado/crear', methods=['POST'])
def crear():
    datos = {
        "nit":             request.form.get('nit'),
        "razon_social":    request.form.get('razon_social'),
        "nombre_contacto": request.form.get('nombre_contacto'),
        "correo":          request.form.get('correo'),
        "telefono":        request.form.get('telefono'),
        "ciudad":          request.form.get('ciudad')
    }
    exito, mensaje = api.crear(TABLA, datos)
    flash(mensaje, 'success' if exito else 'danger')
    return redirect(url_for('aliado.index'))

@aliado_bp.route('/aliado/actualizar', methods=['POST'])
def actualizar():
    nit = request.form.get('nit')
    datos = {
        "razon_social":    request.form.get('razon_social'),
        "nombre_contacto": request.form.get('nombre_contacto'),
        "correo":          request.form.get('correo'),
        "telefono":        request.form.get('telefono'),
        "ciudad":          request.form.get('ciudad')
    }
    exito, mensaje = api.actualizar(TABLA, CLAVE, nit, datos)
    flash(mensaje, 'success' if exito else 'danger')
    return redirect(url_for('aliado.index'))

@aliado_bp.route('/aliado/eliminar', methods=['POST'])
def eliminar():
    nit = request.form.get('nit')
    exito, mensaje = api.eliminar(TABLA, CLAVE, nit)
    flash(mensaje, 'success' if exito else 'danger')
    return redirect(url_for('aliado.index'))