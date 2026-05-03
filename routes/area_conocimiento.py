from flask import Blueprint, render_template, request, redirect, url_for, flash
import requests
from services import ApiService
area_con_bp = Blueprint('area_conocimiento', __name__)
API_URL = "http://127.0.0.1:8000/api/area_conocimiento"

@area_con_bp.route('/')
def index():
    try:
        response = requests.get(API_URL)
        datos = response.json().get('datos', []) if response.status_code == 200 else []
        return render_template('pages/area_conocimiento.html', areas=datos)
    except Exception:
        return render_template('pages/area_conocimiento.html', areas=[])

@area_con_bp.route('/crear', methods=['GET', 'POST'])
def crear():
    if request.method == 'POST':
        data = {
            "gran_area": request.form.get('gran_area'),
            "area": request.form.get('area'),
            "disciplina": request.form.get('disciplina')
        }
        response = requests.post(API_URL, json=data)
        if response.status_code == 201:
            flash("Área creada con éxito", "success")
            return redirect(url_for('area_conocimiento.index'))
        flash("Error al crear área", "danger")
    return render_template('pages/crear_area_conocimiento.html')