from flask import Blueprint, render_template, request, redirect, url_for, flash
import requests

activ_academica_bp = Blueprint('activ_academica', __name__)

# URL de tu API de FastAPI (ajusta el puerto si es necesario)
API_URL = "http://127.0.0.1:8000/api/activ_academica"

@activ_academica_bp.route('/crear', methods=['GET', 'POST'])
def crear():
    if request.method == 'POST':
        # Capturamos los datos del formulario de Flask
        nueva_actividad = {
            "nombre": request.form.get('nombre'),
            "num_creditos": int(request.form.get('num_creditos')),
            "tipo": request.form.get('tipo'),
            "area_formacion": request.form.get('area_formacion'),
            "h_acom": int(request.form.get('h_acom')),
            "h_indep": int(request.form.get('h_indep')),
            "idioma": request.form.get('idioma'),
            "espejo": int(request.form.get('espejo')),
            "entidad_espejo": request.form.get('entidad_espejo', ''),
            "pais_espejo": request.form.get('pais_espejo', ''),
            "disenio": None # O el ID del programa si ya tienes ese select
        }
        
        # Enviamos a la API de FastAPI
        response = requests.post(API_URL, json=nueva_actividad)
        
        if response.status_code == 201:
            flash("Actividad creada exitosamente", "success")
            return redirect(url_for('activ_academica.index'))
        else:
            flash(f"Error al crear: {response.json().get('detail')}", "danger")

    return render_template('pages/crear_activ_academica.html')

@activ_academica_bp.route('/')
def index():
    try:
        response = requests.get(API_URL)
        
        if response.status_code == 204:
            return render_template('pages/activ_academica.html', actividades=[])
            
        if response.status_code == 200:
            data_json = response.json()
            datos = data_json.get('datos', [])
            return render_template('pages/activ_academica.html', actividades=datos)
        
        return render_template('pages/activ_academica.html', actividades=[])

    except Exception as e:
        print(f"DEBUG ERROR: {e}") 
        return render_template('pages/activ_academica.html', actividades=[])