from flask import Blueprint, render_template, request, redirect, url_for, flash
import requests

rol_bp = Blueprint('rol', __name__)

API_URL = "http://127.0.0.1:8000/api/rol"

@rol_bp.route('/')
def index():
    try:
        response = requests.get(API_URL)
        datos = response.json().get('datos', []) if response.status_code == 200 else []
        return render_template('pages/rol.html', roles=datos)
    except Exception as e:
        print(f"Error Rol: {e}")
        return render_template('pages/rol.html', roles=[])

@rol_bp.route('/crear', methods=['GET', 'POST'])
def crear():
    if request.method == 'POST':
        nuevo_rol = {
            "nombre": request.form.get('nombre'),
            "descripcion": request.form.get('descripcion'),
            "activo": True if request.form.get('activo') else False
        }
        response = requests.post(API_URL, json=nuevo_rol)
        if response.status_code == 201:
            flash("Rol creado exitosamente", "success")
            return redirect(url_for('rol.index'))
        flash("Error al crear el rol", "danger")
    
    return render_template('pages/crear_rol.html')