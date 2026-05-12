from flask import Blueprint, render_template, request, redirect, url_for, flash
from services import ApiService

acreditacion_bp = Blueprint("acreditacion", __name__)
api = ApiService()
TABLA = "acreditacion"
CLAVE = "resolucion"

@acreditacion_bp.route("/acreditacion")
def index():
    limite = request.args.get("limite")
    accion = request.args.get("accion")
    clave = request.args.get("clave")

    registros = api.listar(TABLA, limite=limite)

    registro_editar = None
    if accion == "editar" and clave:
        registro_editar = api.get(TABLA, clave)  # ← api.get, no api.obtener

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
        "resolucion":  int(request.form.get("resolucion")),
        "tipo":        request.form.get("tipo"),
        "calificacion": request.form.get("calificacion"),
        "programa":    int(request.form.get("programa")),
        "fecha_inicio": request.form.get("fecha_inicio"),
        "fecha_fin":   request.form.get("fecha_fin")
    }
    exito, mensaje = api.crear(TABLA, datos)
    flash(mensaje, "success" if exito else "danger")
    return redirect(url_for("acreditacion.index"))

@acreditacion_bp.route("/acreditacion/actualizar", methods=["POST"])
def actualizar():
    resolucion = request.form.get("resolucion")
    datos = {
        "tipo":        request.form.get("tipo"),
        "calificacion": request.form.get("calificacion"),
        "programa":    int(request.form.get("programa")),
        "fecha_inicio": request.form.get("fecha_inicio"),
        "fecha_fin":   request.form.get("fecha_fin")
    }
    # ← firma correcta: (tabla, clave_nombre, valor_id, datos)
    exito, mensaje = api.actualizar(TABLA, CLAVE, resolucion, datos)
    flash(mensaje, "success" if exito else "danger")
    return redirect(url_for("acreditacion.index"))

@acreditacion_bp.route("/acreditacion/eliminar", methods=["POST"])
def eliminar():
    resolucion = request.form.get("resolucion")
    # ← firma correcta: (tabla, clave_nombre, valor_id)
    exito, mensaje = api.eliminar(TABLA, CLAVE, resolucion)
    flash(mensaje, "success" if exito else "danger")
    return redirect(url_for("acreditacion.index"))