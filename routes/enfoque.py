from flask import Blueprint, render_template, request, redirect, url_for, flash
import requests
from services import ApiService
enfoque_bp = Blueprint('enfoque', __name__)

API_URL = "http://127.0.0.1:8000/api/enfoque"

@enfoque_bp.route('/')
def index():
    try:
        response = requests.get(API_URL)
        datos = response.json().get('datos', []) if response.status_code == 200 else []
        return render_template('pages/enfoque.html', enfoques=datos)
    except Exception as e:
        print(f"Error Enfoque: {e}")
        return render_template('pages/enfoque.html', enfoques=[])

@enfoque_bp.route('/crear', methods=['GET', 'POST'])
def crear():
    if request.method == 'POST':
        nuevo_enfoque = {
            "nombre": request.form.get('nombre'),
            "descripcion": request.form.get('descripcion')
        }
        response = requests.post(API_URL, json=nuevo_enfoque)
        if response.status_code == 201:
            flash("Enfoque creado con éxito", "success")
            return redirect(url_for('enfoque.index'))
        flash("Error al crear el enfoque", "danger")
    
    return render_template('pages/crear_enfoque.html')