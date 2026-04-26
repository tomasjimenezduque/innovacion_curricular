from flask import Blueprint, render_template, request, redirect, url_for, flash
import requests

alianza_bp = Blueprint('alianza', __name__)

API_URL_ALIANZA = "http://127.0.0.1:8000/api/alianza"
API_URL_ALIADO = "http://127.0.0.1:8000/api/aliado"
# Ajusta esta URL según cómo se llame tu API de programas/departamentos
API_URL_PROGRAMA = "http://127.0.0.1:8000/api/programa" 

@alianza_bp.route('/')
def index():
    try:
        response = requests.get(API_URL_ALIANZA)
        alianzas = []
        if response.status_code == 200:
            alianzas = response.json().get('datos', [])
        return render_template('pages/alianza.html', alianzas=alianzas)
    except Exception as e:
        print(f"Error Alianza: {e}")
        return render_template('pages/alianza.html', alianzas=[])

@alianza_bp.route('/crear', methods=['GET', 'POST'])
def crear():
    if request.method == 'POST':
        nueva_alianza = {
            "aliado": int(request.form.get('aliado')),
            "departamento": int(request.form.get('departamento')),
            "fecha_inicio": request.form.get('fecha_inicio'),
            "fecha_fin": request.form.get('fecha_fin') or None,
            "docente": int(request.form.get('docente')) if request.form.get('docente') else None
        }
        response = requests.post(API_URL_ALIANZA, json=nueva_alianza)
        if response.status_code == 201:
            flash("Alianza creada con éxito", "success")
            return redirect(url_for('alianza.index'))
        flash("Error al crear la alianza", "danger")

    # Necesitamos cargar los selectores para elegir Aliado y Programa
    aliados = requests.get(API_URL_ALIADO).json().get('datos', [])
    programas = requests.get(API_URL_PROGRAMA).json().get('datos', [])
    
    return render_template('pages/crear_alianza.html', aliados=aliados, programas=programas)