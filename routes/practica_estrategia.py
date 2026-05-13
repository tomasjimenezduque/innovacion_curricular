from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.api_service import ApiService

practica_est_bp = Blueprint('practica_estrategia', __name__)
api = ApiService()
TABLA = 'practica_estrategia'
CLAVE = 'id'

@practica_est_bp.route('/practica_estrategia')
def index():
    accion = request.args.get('accion')
    id_p = request.args.get('id')

    practicas = api.listar(TABLA)

    practica_editar = None
    if accion == 'editar' and id_p:
        practica_editar = api.get(TABLA, id_p)

    return render_template('pages/practica_estrategia.html',
                           practicas=practicas,
                           accion=accion,
                           practica_editar=practica_editar)

@practica_est_bp.route('/practica_estrategia/crear', methods=['POST'])
def crear():
    datos = {
        "tipo":        request.form.get('tipo'),
        "nombre":      request.form.get('nombre'),
        "descripcion": request.form.get('descripcion')
    }
    exito, mensaje = api.crear(TABLA, datos)
    flash(mensaje, 'success' if exito else 'danger')
    return redirect(url_for('practica_estrategia.index'))

@practica_est_bp.route('/practica_estrategia/actualizar', methods=['POST'])
def actualizar():
    id_p = request.form.get('id')
    datos = {
        "tipo":        request.form.get('tipo'),
        "nombre":      request.form.get('nombre'),
        "descripcion": request.form.get('descripcion')
    }
    exito, mensaje = api.actualizar(TABLA, CLAVE, id_p, datos)
    flash(mensaje, 'success' if exito else 'danger')
    return redirect(url_for('practica_estrategia.index'))

@practica_est_bp.route('/practica_estrategia/eliminar', methods=['POST'])
def eliminar():
    id_p = request.form.get('id')
    exito, mensaje = api.eliminar(TABLA, CLAVE, id_p)
    flash(mensaje, 'success' if exito else 'danger')
    return redirect(url_for('practica_estrategia.index'))