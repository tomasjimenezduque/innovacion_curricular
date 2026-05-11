from flask import Blueprint, render_template, request, redirect, url_for, flash
import requests

docente_dept_bp = Blueprint('docente_departamento', __name__)

API_URL_DD = "http://127.0.0.1:8000/api/docente_departamento"
API_URL_PROG = "http://127.0.0.1:8000/api/programa"

@docente_dept_bp.route('/')
def index():
    try:
        response = requests.get(API_URL_DD)
        datos = response.json().get('datos', []) if response.status_code == 200 else []
        return render_template('pages/docente_departamento.html', registros=datos)
    except Exception as e:
        print(f"Error Docente Dept: {e}")
        return render_template('pages/docente_departamento.html', registros=[])

@docente_dept_bp.route('/crear', methods=['GET', 'POST'])
def crear():
    if request.method == 'POST':
        data = {
            "docente": int(request.form.get('docente')),
            "departamento": int(request.form.get('departamento')),
            "dedicacion": request.form.get('dedicacion'),
            "modalidad": request.form.get('modalidad'),
            "fecha_ingreso": request.form.get('fecha_ingreso'),
            "fecha_salida": request.form.get('fecha_salida') or None
        }
        response = requests.post(API_URL_DD, json=data)
        if response.status_code == 201:
            flash("Asignación de docente creada con éxito", "success")
            return redirect(url_for('docente_departamento.index'))
        flash("Error al asignar docente", "danger")

    # Cargamos programas para el selector
    programas = requests.get(API_URL_PROG).json().get('datos', [])
    return render_template('pages/crear_docente_departamento.html', programas=programas)