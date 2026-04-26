from flask import Blueprint, render_template, request, redirect, url_for, flash
from services import ApiService

acreditacion_bp = Blueprint("acreditacion", __name__)
api = ApiService()

@acreditacion_bp.route("/acreditacion")
def index():
    limite = request.args.get("limite")
    accion = request.args.get("accion")
    clave = request.args.get("clave")

    # Obtener lista de acreditaciones
    registros = api.listar("acreditacion", limite=limite)

    registro_editar = None
    if accion == "editar" and clave:
        registro_editar = api.obtener("acreditacion", clave)

    return render_template(
        "pages/acreditacion.html",
        registros=registros,
        accion=accion,
        registro_editar=registro_editar,
        limite=limite
    )

@acreditacion_bp.route("/acreditacion/crear", methods=["POST"])
def crear():
    datos = {
        "resolucion": int(request.form.get("resolucion", 0)),
        "tipo": request.form.get("tipo"),
        "calificacion": request.form.get("calificacion"),
        "programa": int(request.form.get("programa", 0)),
        "fecha_inicio": request.form.get("fecha_inicio"),
        "fecha_fin": request.form.get("fecha_fin")
    }
    exito, mensaje = api.crear("acreditacion", datos)
    flash(mensaje, "success" if exito else "danger")
    return redirect(url_for("acreditacion.index"))

@acreditacion_bp.route("/acreditacion/actualizar", methods=["POST"])
def actualizar():
    resolucion = request.form.get("resolucion")
    datos = {
        "resolucion": int(resolucion),
        "tipo": request.form.get("tipo"),
        "calificacion": request.form.get("calificacion"),
        "programa": int(request.form.get("programa", 0)),
        "fecha_inicio": request.form.get("fecha_inicio"),
        "fecha_fin": request.form.get("fecha_fin")
    }
    exito, mensaje = api.actualizar("acreditacion", resolucion, datos)
    flash(mensaje, "success" if exito else "danger")
    return redirect(url_for("acreditacion.index"))

@acreditacion_bp.route("/acreditacion/eliminar", methods=["POST"])
def eliminar():
    resolucion = request.form.get("resolucion")
    exito, mensaje = api.eliminar("acreditacion", resolucion)
    flash(mensaje, "success" if exito else "danger")
    return redirect(url_for("acreditacion.index"))