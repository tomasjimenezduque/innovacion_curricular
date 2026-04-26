from flask import Blueprint, render_template, request, redirect, url_for, flash
import requests

practica_est_bp = Blueprint('practica_estrategia', __name__)

API_URL = "http://127.0.0.1:8000/api/practica_estrategia"

@practica_est_bp.route('/')
def index():
    try:
        response = requests.get(API_URL)
        datos = response.json().get('datos', []) if response.status_code == 200 else []
        return render_template('pages/practica_estrategia.html', practicas=datos)
    except Exception as e:
        print(f"Error Práctica Estratégica: {e}")
        return render_template('pages/practica_estrategia.html', practicas=[])

@practica_est_bp.route('/crear', methods=['GET', 'POST'])
def crear():
    if request.method == 'POST':
        nueva_practica = {
            "tipo": request.form.get('tipo'),
            "nombre": request.form.get('nombre'),
            "descripcion": request.form.get('descripcion')
        }
        response = requests.post(API_URL, json=nueva_practica)
        if response.status_code == 201:
            flash("Práctica estratégica creada con éxito", "success")
            return redirect(url_for('practica_estrategia.index'))
        flash("Error al registrar la práctica", "danger")
    
    return render_template('pages/crear_practica_estrategia.html')