from flask import Blueprint, render_template, request, redirect, url_for, flash
import requests

programa_bp = Blueprint('programa', __name__)

API_URL_PROG = "http://127.0.0.1:8000/api/programa"
API_URL_FAC = "http://127.0.0.1:8000/api/facultad"

@programa_bp.route('/')
def index():
    try:
        response = requests.get(API_URL_PROG)
        datos = response.json().get('datos', []) if response.status_code == 200 else []
        return render_template('pages/programa.html', programas=datos)
    except Exception as e:
        print(f"Error Programa: {e}")
        return render_template('pages/programa.html', programas=[])

@programa_bp.route('/crear', methods=['GET', 'POST'])
def crear():
    if request.method == 'POST':
        data = {
            "nombre": request.form.get('nombre'),
            "tipo": request.form.get('tipo'),
            "nivel": request.form.get('nivel'),
            "fecha_creacion": request.form.get('fecha_creacion'),
            "numero_cohortes": request.form.get('numero_cohortes'),
            "cant_graduados": request.form.get('cant_graduados'),
            "fecha_actualizacion": request.form.get('fecha_actualizacion'),
            "ciudad": request.form.get('ciudad'),
            "facultad": int(request.form.get('facultad')),
            "fecha_cierre": request.form.get('fecha_cierre') or None
        }
        response = requests.post(API_URL_PROG, json=data)
        if response.status_code == 201:
            flash("Programa creado con éxito", "success")
            return redirect(url_for('programa.index'))
        flash("Error al crear programa", "danger")

    # Cargamos facultades para el selector
    facultades = requests.get(API_URL_FAC).json().get('datos', [])
    return render_template('pages/crear_programa.html', facultades=facultades)