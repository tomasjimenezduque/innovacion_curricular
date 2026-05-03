from flask import Blueprint, render_template, request, redirect, url_for, flash

from services import ApiService



# ─── Crear el Blueprint para Universidad ───────────────────

universidad_bp = Blueprint("universidad", __name__)

api = ApiService()



# ═══════════════════════════════════════════════════════════════

#  RUTA PRINCIPAL — Listar + mostrar formularios

# ═══════════════════════════════════════════════════════════════

@universidad_bp.route("/universidad")

def index():

    """

    Muestra la lista de universidades y los formularios de CRUD.

    """

    limite = request.args.get("limite")

    accion = request.args.get("accion") # "nuevo", "editar" o None

    id_u = request.args.get("id")       # Usamos 'id' como clave para universidad



    # Consultamos al Backend (FastAPI) a través del ApiService

    universidades = api.listar("universidad", limite=limite)



    universidad_editar = None

    if accion == "editar" and id_u:

        universidad_editar = api.get("universidad", id_u)



    return render_template(

        "pages/universidad.html",

        universidades=universidades,

        accion=accion,

        universidad_editar=universidad_editar,

        limite=limite

    )



# ═══════════════════════════════════════════════════════════════

#  CREAR — Recibir formulario y enviar a la API

# ═══════════════════════════════════════════════════════════════

@universidad_bp.route("/universidad/crear", methods=["POST"])

def crear():

    # Debemos capturar los nombres EXACTOS que el HTML envía

    # y que el Modelo de SQLAlchemy espera.

    datos = {

        "id": request.form.get("id"),

        "nombre": request.form.get("nombre"),

        "ciudad": request.form.get("ciudad"),  # CAMBIADO: Antes decía 'ubicacion'

        "tipo": request.form.get("tipo")       # AGREGADO: Para que no vaya vacío

    }

   

    exito, mensaje = api.crear("universidad", datos)

    flash(mensaje, "success" if exito else "danger")

    return redirect(url_for("universidad.index"))



# ═══════════════════════════════════════════════════════════════

#  ACTUALIZAR — Enviar cambios a la API

# ═══════════════════════════════════════════════════════════════

# universidad_routes.py (en el proyecto FRONT/FLASK)



@universidad_bp.route('/actualizar', methods=['POST'])
def actualizar():
    # 1. Obtenemos los datos del formulario
    data = request.form.to_dict()
    
    # 2. Extraemos el ID para la URL
    id_uni = data.pop('id', None)
    
    if not id_uni:
        flash("Error: No se encontró el ID de la universidad", "danger")
        return redirect(url_for('universidad.index'))

    # 3. Llamada al API Service respetando los 4 argumentos:
    # tabla="universidad", clave_nombre="id", valor_id=id_uni, datos=data
    exito, mensaje = api.actualizar(
        "universidad",  # tabla
        "id",           # clave_nombre (por compatibilidad)
        id_uni,         # valor_id
        data            # datos (el diccionario sin el ID)
    )
    
    flash(mensaje, 'success' if exito else 'danger')
    return redirect(url_for('universidad.index'))



@universidad_bp.route('/eliminar', methods=['POST'])
def eliminar():
    # 1. Obtenemos el ID del formulario
    id_uni = request.form.get('id')
    
    if not id_uni:
        flash("Error: No se pudo encontrar el ID de la universidad", "danger")
        return redirect(url_for('universidad.index'))

    # 2. Llamada corregida al ApiService
    # Según tu ApiService: def eliminar(self, recurso, valor_id, nombre_clave):
    exito, mensaje = api.eliminar(
        "universidad", # recurso/tabla
        id_uni,        # valor_id
        "id"           # nombre_clave
    )
    
    flash(mensaje, 'success' if exito else 'danger')
    return redirect(url_for('universidad.index'))