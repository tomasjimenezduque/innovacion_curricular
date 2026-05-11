from flask import Blueprint, render_template, request, redirect, url_for, flash
import requests

aspecto_normativo_bp = Blueprint('aspecto_normativo', __name__)

API_URL = "http://127.0.0.1:8000/api/aspecto_normativo"

@aspecto_normativo_bp.route('/')
def index():
    try:
        response = requests.get(API_URL)
        datos = response.json().get('datos', []) if response.status_code == 200 else []
        return render_template('pages/aspecto_normativo.html', aspectos=datos)
    except Exception as e:
        print(f"Error Aspecto Normativo: {e}")
        return render_template('pages/aspecto_normativo.html', aspectos=[])

@aspecto_normativo_bp.route('/crear', methods=['GET', 'POST'])
def crear():
    if request.method == 'POST':
        nueva_norma = {
            "tipo": request.form.get('tipo'),
            "descripcion": request.form.get('descripcion'),
            "fuente": request.form.get('fuente')
        }
        response = requests.post(API_URL, json=nueva_norma)
        if response.status_code == 201:
            flash("Aspecto Normativo creado con éxito", "success")
            return redirect(url_for('aspecto_normativo.index'))
        flash("Error al crear el registro", "danger")
    
    return render_template('pages/crear_aspecto_normativo.html')