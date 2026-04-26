from flask import Blueprint, render_template, request, redirect, url_for, flash
import requests

aliado_bp = Blueprint('aliado', __name__)

API_URL = "http://127.0.0.1:8000/api/aliado"

@aliado_bp.route('/')
def index():
    try:
        response = requests.get(API_URL)
        if response.status_code == 204:
            return render_template('pages/aliado.html', aliados=[])
        
        if response.status_code == 200:
            data = response.json()
            return render_template('pages/aliado.html', aliados=data.get('datos', []))
        
        return render_template('pages/aliado.html', aliados=[])
    except Exception as e:
        print(f"Error Aliado: {e}")
        return render_template('pages/aliado.html', aliados=[])

@aliado_bp.route('/crear', methods=['GET', 'POST'])
def crear():
    if request.method == 'POST':
        nuevo_aliado = {
            "nit": int(request.form.get('nit')),
            "razon_social": request.form.get('razon_social'),
            "nombre_contacto": request.form.get('nombre_contacto'),
            "correo": request.form.get('correo'),
            "telefono": request.form.get('telefono'),
            "ciudad": request.form.get('ciudad')
        }
        response = requests.post(API_URL, json=nuevo_aliado)
        if response.status_code == 201:
            flash("Aliado registrado con éxito", "success")
            return redirect(url_for('aliado.index'))
        flash("Error al registrar aliado", "danger")
    
    return render_template('pages/crear_aliado.html')