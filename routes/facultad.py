from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.api_service import ApiService
from services.abstracciones.i_api_service import IApiService

# Definición del Blueprint y del servicio siguiendo SOLID
facultad_bp = Blueprint("facultad", __name__)
api: IApiService = ApiService()

@facultad_bp.route("/facultad")
def index():
    """
    Renderiza el listado y maneja la lógica de cargar datos para editar
    basado en los parámetros de la URL (?accion=editar&id=X).
    """
    accion = request.args.get("accion")
    id_editar = request.args.get("id")
    facultad_editar = None
    
    # Si la acción es editar, recuperamos la facultad específica
    if accion == "editar" and id_editar:
        facultad_editar = api.get("facultad", id_editar)
        if not facultad_editar:
            flash("No se pudo obtener la facultad para editar", "warning")
        
    facultades = api.listar("facultad")
    return render_template("pages/facultad.html", 
                           facultades=facultades, 
                           accion=accion, 
                           facultad_editar=facultad_editar)

@facultad_bp.route("/facultad/crear", methods=["POST"])
def crear():
    """Maneja el POST para crear una nueva facultad."""
    datos = {
        "nombre": request.form.get("nombre"),
        "tipo": request.form.get("tipo"),
        "fecha_fun": request.form.get("fecha_fun"),
        "universidad": request.form.get("universidad")
    }
    
    exito, mensaje = api.crear("facultad", datos)
    if exito:
        flash("Facultad creada exitosamente", "success")
    else:
        flash(f"Error al crear: {mensaje}", "danger")
    
    return redirect(url_for("facultad.index"))

@facultad_bp.route("/facultad/editar/<int:id>", methods=["POST"])
def editar(id):
    """Maneja la actualización con conversión de tipos."""
    try:
        # El formulario envía strings, convertimos universidad a entero
        datos = {
            "nombre": request.form.get("nombre"),
            "tipo": request.form.get("tipo"),
            "fecha_fun": request.form.get("fecha_fun"),
            "universidad": int(request.form.get("universidad")) # <-- CAMBIO AQUÍ
        }
        
        exito, mensaje = api.actualizar("facultad", "id", id, datos)
        
        if exito:
            flash("Facultad actualizada correctamente", "success")
        else:
            flash(f"Error al actualizar: {mensaje}", "danger")
            
    except ValueError:
        flash("Error: El ID de la universidad debe ser un número.", "warning")
        
    return redirect(url_for("facultad.index"))

@facultad_bp.route("/facultad/eliminar/<int:id>", methods=["POST"])
def eliminar(id):
    """Maneja la eliminación mediante POST."""
    exito, mensaje = api.eliminar("facultad", "id", id)
    if exito:
        flash("Facultad eliminada", "success")
    else:
        flash(f"No se pudo eliminar: {mensaje}", "danger")
        
    return redirect(url_for("facultad.index"))