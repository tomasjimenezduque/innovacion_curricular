from flask import Blueprint, render_template, request, redirect, url_for, flash
import requests

premio_bp = Blueprint('premio', __name__)

API_URL_PREMIO = "http://127.0.0.1:8000/api/premio"
API_URL_PROG = "http://127.0.0.1:8000/api/programa"

@premio_bp.route('/')
def index():
    try:
        response = requests.get(API_URL_PREMIO)
        datos = response.json().get('datos', []) if response.status_code == 200 else []
        return render_template('pages/premio.html', premios=datos)
    except Exception as e:
        print(f"Error Premio: {e}")
        return render_template('pages/premio.html', premios=[])

@premio_bp.route('/crear', methods=['GET', 'POST'])
def crear():
    if request.method == 'POST':
        data = {
            "nombre": request.form.get('nombre'),
            "descripcion": request.form.get('descripcion'),
            "fecha": request.form.get('fecha'),
            "entidad_otorgante": request.form.get('entidad_otorgante'),
            "pais": request.form.get('pais'),
            "programa": int(request.form.get('programa'))
        }
        response = requests.post(API_URL_PREMIO, json=data)
        if response.status_code == 201:
            flash("Premio registrado con éxito", "success")
            return redirect(url_for('premio.index'))
        flash("Error al registrar el premio", "danger")

    try:
        programas = requests.get(API_URL_PROG).json().get('datos', [])
    except:
        programas = []
        
    return render_template('pages/crear_premio.html', programas=programas)