from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.api_service import ApiService
import bcrypt  # agregar este import arriba

# CAMBIO CLAVE: El nombre de la variable debe ser 'usuario_bp' para que app.py lo reconozca
usuario_bp = Blueprint('usuario', __name__)
api = ApiService()
TABLA = 'usuario'
CLAVE = 'id' 

@usuario_bp.route('/usuario')
def index():
    limite = request.args.get('limite', type=int)
    accion = request.args.get('accion', '')
    valor_id = request.args.get('id', '')

    registros = api.listar(TABLA, limite)
    mostrar_formulario = accion in ('nuevo', 'editar')
    editando = accion == 'editar'

    registro = None
    if editando and valor_id:
        registro = next(
            (r for r in registros if str(r.get(CLAVE)) == valor_id), None
        )

    return render_template(
        'pages/usuario.html',
        registros=registros, 
        mostrar_formulario=mostrar_formulario,
        editando=editando, 
        registro=registro, 
        limite=limite
    )

@usuario_bp.route('/usuario/crear', methods=['POST'])
def crear():
    password_plano = request.form.get('password')
    password_hash = bcrypt.hashpw(password_plano.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    datos = {
        'username':        request.form.get('username'),
        'email':           request.form.get('email'),
        'password':        password_hash,  # ya encriptado
        'nombre_completo': request.form.get('nombre_completo'),
        'activo':          'activo' in request.form
    }
    
    exito, mensaje = api.crear(TABLA, datos)  # sin kwargs
    
    flash(mensaje, 'success' if exito else 'danger')
    return redirect(url_for('usuario.index'))


@usuario_bp.route('/usuario/actualizar', methods=['POST'])
def actualizar():
    valor_id = request.form.get('id', '')
    datos = {
        'username':        request.form.get('username'),
        'email':           request.form.get('email'),
        'nombre_completo': request.form.get('nombre_completo'),
        'activo':          'activo' in request.form
    }
    
    password_nuevo = request.form.get('password')
    if password_nuevo:  # solo encriptar si viene uno nuevo
        datos['password'] = bcrypt.hashpw(
            password_nuevo.encode('utf-8'), bcrypt.gensalt()
        ).decode('utf-8')

    exito, mensaje = api.actualizar(TABLA, CLAVE, valor_id, datos)  # sin kwargs
    
    flash(mensaje, 'success' if exito else 'danger')
    return redirect(url_for('usuario.index'))

@usuario_bp.route('/usuario/eliminar', methods=['POST'])
def eliminar():
    valor_id = request.form.get('id', '')
    exito, mensaje = api.eliminar(TABLA, CLAVE, valor_id)
    
    flash(mensaje, 'success' if exito else 'danger')
    return redirect(url_for('usuario.index'))