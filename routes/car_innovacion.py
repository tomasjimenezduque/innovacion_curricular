from flask import Blueprint, render_template, request, redirect, url_for, flash
import requests

car_innovacion_bp = Blueprint('car_innovacion', __name__)

API_URL = "http://127.0.0.1:8000/api/car_innovacion"

@car_innovacion_bp.route('/')
def index():
    try:
        response = requests.get(API_URL)
        datos = response.json().get('datos', []) if response.status_code == 200 else []
        return render_template('pages/car_innovacion.html', innovaciones=datos)
    except Exception as e:
        print(f"Error Característica Innovación: {e}")
        return render_template('pages/car_innovacion.html', innovaciones=[])

@car_innovacion_bp.route('/crear', methods=['GET', 'POST'])
def crear():
    if request.method == 'POST':
        nueva_car = {
            "nombre": request.form.get('nombre'),
            "descripcion": request.form.get('descripcion'),
            "tipo": request.form.get('tipo')
        }
        response = requests.post(API_URL, json=nueva_car)
        if response.status_code == 201:
            flash("Característica de innovación creada", "success")
            return redirect(url_for('car_innovacion.index'))
        flash("Error al registrar característica", "danger")
    
    return render_template('pages/crear_car_innovacion.html')