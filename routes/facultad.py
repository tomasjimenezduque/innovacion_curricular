from flask import Blueprint, render_template, request, redirect, url_for, flash
import requests

facultad_bp = Blueprint('facultad', __name__)

API_URL_FAC = "http://127.0.0.1:8000/api/facultad"
API_URL_UNI = "http://127.0.0.1:8000/api/universidad"

@facultad_bp.route('/')
def index():
    try:
        response = requests.get(API_URL_FAC)
        datos = response.json().get('datos', []) if response.status_code == 200 else []
        return render_template('pages/facultad.html', facultades=datos)
    except Exception as e:
        print(f"Error Facultad: {e}")
        return render_template('pages/facultad.html', facultades=[])

@facultad_bp.route('/crear', methods=['GET', 'POST'])
def crear():
    if request.method == 'POST':
        data = {
            "nombre": request.form.get('nombre'),
            "tipo": request.form.get('tipo'),
            "fecha_fun": request.form.get('fecha_fun'),
            "universidad": int(request.form.get('universidad'))
        }
        response = requests.post(API_URL_FAC, json=data)
        if response.status_code == 201:
            flash("Facultad creada con éxito", "success")
            return redirect(url_for('facultad.index'))
        flash("Error al crear facultad", "danger")

    # Intentamos cargar universidades para el selector
    try:
        universidades = requests.get(API_URL_UNI).json().get('datos', [])
    except:
        universidades = []
        
    return render_template('pages/crear_facultad.html', universidades=universidades)