from flask import Blueprint, render_template, request, redirect, url_for, flash
import requests

rc_bp = Blueprint('registro_calificado', __name__)

API_URL_RC = "http://127.0.0.1:8000/api/registro_calificado"
API_URL_PROG = "http://127.0.0.1:8000/api/programa"

@rc_bp.route('/')
def index():
    try:
        response = requests.get(API_URL_RC)
        datos = response.json().get('datos', []) if response.status_code == 200 else []
        return render_template('pages/registro_calificado.html', registros=datos)
    except Exception as e:
        print(f"Error Registro Calificado: {e}")
        return render_template('pages/registro_calificado.html', registros=[])

@rc_bp.route('/crear', methods=['GET', 'POST'])
def crear():
    if request.method == 'POST':
        data = {
            "codigo": int(request.form.get('codigo')),
            "cant_creditos": request.form.get('cant_creditos'),
            "hora_acom": request.form.get('hora_acom'),
            "hora_ind": request.form.get('hora_ind'),
            "metodologia": request.form.get('metodologia'),
            "fecha_inicio": request.form.get('fecha_inicio'),
            "fecha_fin": request.form.get('fecha_fin'),
            "duracion_anios": request.form.get('duracion_anios'),
            "duracion_semestres": request.form.get('duracion_semestres'),
            "tipo_titulacion": request.form.get('tipo_titulacion'),
            "programa": int(request.form.get('programa'))
        }
        response = requests.post(API_URL_RC, json=data)
        if response.status_code == 201:
            flash("Registro Calificado creado con éxito", "success")
            return redirect(url_for('registro_calificado.index'))
        
        error_detail = response.json().get('detail', "Error desconocido")
        flash(f"Error: {error_detail}", "danger")

    try:
        programas = requests.get(API_URL_PROG).json().get('datos', [])
    except:
        programas = []
        
    return render_template('pages/crear_registro_calificado.html', programas=programas)