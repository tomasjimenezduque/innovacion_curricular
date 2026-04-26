from flask import Blueprint, render_template, request, redirect, url_for, flash
import requests

pasantia_bp = Blueprint('pasantia', __name__)

API_URL_PAS = "http://127.0.0.1:8000/api/pasantia"
API_URL_PROG = "http://127.0.0.1:8000/api/programa"

@pasantia_bp.route('/')
def index():
    try:
        response = requests.get(API_URL_PAS)
        datos = response.json().get('datos', []) if response.status_code == 200 else []
        return render_template('pages/pasantia.html', pasantias=datos)
    except Exception as e:
        print(f"Error Pasantía: {e}")
        return render_template('pages/pasantia.html', pasantias=[])

@pasantia_bp.route('/crear', methods=['GET', 'POST'])
def crear():
    if request.method == 'POST':
        data = {
            "nombre": request.form.get('nombre'),
            "pais": request.form.get('pais'),
            "empresa": request.form.get('empresa'),
            "descripcion": request.form.get('descripcion'),
            "programa": int(request.form.get('programa'))
        }
        response = requests.post(API_URL_PAS, json=data)
        if response.status_code == 201:
            flash("Pasantía registrada correctamente", "success")
            return redirect(url_for('pasantia.index'))
        flash("Error al registrar la pasantía", "danger")

    # Cargar programas para el select
    try:
        programas = requests.get(API_URL_PROG).json().get('datos', [])
    except:
        programas = []
        
    return render_template('pages/crear_pasantia.html', programas=programas)