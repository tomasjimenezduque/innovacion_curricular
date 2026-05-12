from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.api_service import ApiService

rc_bp = Blueprint('registro_calificado', __name__)
api = ApiService()
TABLA = 'registro_calificado'
CLAVE = 'codigo'

@rc_bp.route('/registro_calificado')
def index():
    accion = request.args.get('accion')
    codigo = request.args.get('id')

    registros = api.listar(TABLA)
    programas = api.listar('programa')

    registro_editar = None
    if accion == 'editar' and codigo:
        registro_editar = api.get(TABLA, codigo)

    return render_template('pages/registro_calificado.html',
                           registros=registros,
                           programas=programas,
                           accion=accion,
                           registro_editar=registro_editar)

@rc_bp.route('/registro_calificado/crear', methods=['POST'])
def crear():
    datos = {
        "codigo":              int(request.form.get('codigo')),
        "cant_creditos":       request.form.get('cant_creditos'),
        "hora_acom":           request.form.get('hora_acom'),
        "hora_ind":            request.form.get('hora_ind'),
        "metodologia":         request.form.get('metodologia'),
        "fecha_inicio":        request.form.get('fecha_inicio'),
        "fecha_fin":           request.form.get('fecha_fin'),
        "duracion_anios":      request.form.get('duracion_anios'),
        "duracion_semestres":  request.form.get('duracion_semestres'),
        "tipo_titulacion":     request.form.get('tipo_titulacion'),
        "programa":            int(request.form.get('programa'))
    }
    exito, mensaje = api.crear(TABLA, datos)
    flash(mensaje, 'success' if exito else 'danger')
    return redirect(url_for('registro_calificado.index'))

@rc_bp.route('/registro_calificado/actualizar', methods=['POST'])
def actualizar():
    codigo = request.form.get('codigo')
    datos = {
        "cant_creditos":       request.form.get('cant_creditos'),
        "hora_acom":           request.form.get('hora_acom'),
        "hora_ind":            request.form.get('hora_ind'),
        "metodologia":         request.form.get('metodologia'),
        "fecha_inicio":        request.form.get('fecha_inicio'),
        "fecha_fin":           request.form.get('fecha_fin'),
        "duracion_anios":      request.form.get('duracion_anios'),
        "duracion_semestres":  request.form.get('duracion_semestres'),
        "tipo_titulacion":     request.form.get('tipo_titulacion'),
        "programa":            int(request.form.get('programa'))
    }
    exito, mensaje = api.actualizar(TABLA, CLAVE, codigo, datos)
    flash(mensaje, 'success' if exito else 'danger')
    return redirect(url_for('registro_calificado.index'))

@rc_bp.route('/registro_calificado/eliminar', methods=['POST'])
def eliminar():
    codigo = request.form.get('codigo')
    exito, mensaje = api.eliminar(TABLA, CLAVE, codigo)
    flash(mensaje, 'success' if exito else 'danger')
    return redirect(url_for('registro_calificado.index'))