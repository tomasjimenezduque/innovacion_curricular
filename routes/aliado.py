from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.api_service import ApiService
from services.abstracciones.i_api_service import IApiService

# Definición del Blueprint y del servicio siguiendo la misma lógica de Facultad
aliado_bp = Blueprint("aliado", __name__)
api: IApiService = ApiService()

@aliado_bp.route("/aliado")
def index():
    """
    Renderiza el listado de aliados y maneja la carga para editar.
    """
    accion = request.args.get("accion")
    id_editar = request.args.get("id") # Este es el NIT
    aliado_editar = None
    
    if accion == "editar" and id_editar:
        # Buscamos el aliado por su NIT
        aliado_editar = api.get("aliado", id_editar)
        if not aliado_editar:
            flash("No se pudo obtener el aliado para editar", "warning")
        
    aliados = api.listar("aliado")
    return render_template("pages/aliado.html", 
                           aliados=aliados, 
                           accion=accion, 
                           aliado_editar=aliado_editar)

@aliado_bp.route("/aliado/crear", methods=["POST"])
def crear():
    """Maneja el registro de un nuevo aliado."""
    datos = {
        "nit": request.form.get("nit"),
        "razon_social": request.form.get("razon_social"),
        "nombre_contacto": request.form.get("nombre_contacto"),
        "correo": request.form.get("correo"),
        "telefono": request.form.get("telefono"),
        "ciudad": request.form.get("ciudad")
    }
    
    exito, mensaje = api.crear("aliado", datos)
    if exito:
        flash("Aliado registrado exitosamente", "success")
    else:
        flash(f"Error al registrar: {mensaje}", "danger")
    
    return redirect(url_for("aliado.index"))

@aliado_bp.route("/aliado/editar/<string:id>", methods=["POST"])
def actualizar(id):
    """
    Maneja la actualización. Nota que usamos <string:id> 
    porque el NIT no siempre es solo números.
    """
    datos = {
        "razon_social": request.form.get("razon_social"),
        "nombre_contacto": request.form.get("nombre_contacto"),
        "correo": request.form.get("correo"),
        "telefono": request.form.get("telefono"),
        "ciudad": request.form.get("ciudad")
    }
    
    # IMPORTANTE: Pasamos "nit" como nombre de la columna clave
    exito, mensaje = api.actualizar("aliado", "nit", id, datos)
    
    if exito:
        flash("Datos del aliado actualizados", "success")
    else:
        flash(f"Error al actualizar: {mensaje}", "danger")
            
    return redirect(url_for("aliado.index"))

@aliado_bp.route("/aliado/eliminar/<string:id>", methods=["POST"])
def eliminar(id):
    exito, mensaje = api.eliminar("aliado", id)
    
    if exito:
        flash("Aliado eliminado correctamente", "success")
    else:
        # Si el error contiene "alianza", es porque hay una restricción
        if "alianza" in mensaje.lower():
            flash("No se puede eliminar: Este aliado tiene alianzas registradas. Primero debe eliminar las alianzas asociadas.", "warning")
        else:
            flash(f"Error: {mensaje}", "danger")
            
    return redirect(url_for("aliado.index"))