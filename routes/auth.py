"""Rutas de autenticacion: login, logout, cambiar y recuperar contrasena.

Adaptado para la API generica FastAPI (sin JWT, sin roles/rutas dinamicos).
Usa POST /api/usuario/verificar-contrasena para login.
"""

import random
import string
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from services.auth_service import AuthService
from services.email_service import enviar_contrasena_temporal


bp = Blueprint("auth", __name__)
auth = AuthService()

_emails_debe_cambiar = set()


def validar_contrasena(pwd):
    if len(pwd) < 6:
        return "La contrasena debe tener al menos 6 caracteres."
    if not any(c.isupper() for c in pwd):
        return "Debe incluir al menos una letra mayuscula."
    if not any(c.isdigit() for c in pwd):
        return "Debe incluir al menos un numero."
    if pwd in ("123", "1234", "12345", "123456"):
        return "No puede usar una contrasena trivial."
    return None


@bp.route("/login", methods=["GET"])
def login():
    if session.get("usuario"):
        return redirect(url_for("home.index"))
    return render_template("pages/login.html")


@bp.route("/login", methods=["POST"])
def login_post():
    email = request.form.get("email", "").strip()
    contrasena = request.form.get("contrasena", "")
    if not email or not contrasena:
        flash("Ingrese email y contrasena.", "danger")
        return render_template("pages/login.html")

    exito, datos = auth.login(email, contrasena)
    if not exito:
        flash(datos.get("mensaje", "Error de autenticacion."), "danger")
        return render_template("pages/login.html")

    datos_usuario = auth.obtener_datos_usuario(email)

    session["usuario"] = email
    session["nombre_usuario"] = datos_usuario.get("nombre", email)

    debe_cambiar = datos_usuario.get("debe_cambiar_contrasena", False)
    if debe_cambiar or email.lower() in _emails_debe_cambiar:
        session["debe_cambiar_contrasena"] = True
        _emails_debe_cambiar.discard(email.lower())
        flash("Debe cambiar su contrasena antes de continuar.", "warning")
        return redirect(url_for("auth.cambiar_contrasena"))

    flash(f"Bienvenido, {session.get('nombre_usuario', email)}", "success")
    return redirect(url_for("home.index"))


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))


@bp.route("/cambiar-contrasena", methods=["GET"])
def cambiar_contrasena():
    return render_template("pages/cambiar_contrasena.html")


@bp.route("/cambiar-contrasena", methods=["POST"])
def cambiar_contrasena_post():
    email = session.get("usuario", "")
    nueva = request.form.get("nueva", "")
    confirmar = request.form.get("confirmar", "")

    if nueva != confirmar:
        flash("Las contrasenas no coinciden.", "danger")
        return render_template("pages/cambiar_contrasena.html")

    error = validar_contrasena(nueva)
    if error:
        flash(error, "danger")
        return render_template("pages/cambiar_contrasena.html")

    exito, mensaje = auth.actualizar_contrasena(email, nueva)
    if exito:
        session.pop("debe_cambiar_contrasena", None)
        flash("Contrasena actualizada exitosamente.", "success")
        return redirect(url_for("home.index"))

    flash(f"Error al actualizar: {mensaje}", "danger")
    return render_template("pages/cambiar_contrasena.html")


@bp.route("/recuperar-contrasena", methods=["GET"])
def recuperar_contrasena():
    return render_template("pages/recuperar_contrasena.html")


@bp.route("/recuperar-contrasena", methods=["POST"])
def recuperar_contrasena_post():
    email = request.form.get("email", "").strip()
    if not email:
        flash("Ingrese su correo electronico.", "danger")
        return render_template("pages/recuperar_contrasena.html")

    datos_usuario = auth.obtener_datos_usuario(email)
    if not datos_usuario:
        flash("No se encontro una cuenta con ese correo.", "danger")
        return render_template("pages/recuperar_contrasena.html")

    pwd = "".join([random.choice(string.ascii_uppercase), random.choice(string.ascii_lowercase),
                   random.choice(string.digits)] + random.choices(string.ascii_letters + string.digits, k=5))

    exito, mensaje = auth.actualizar_contrasena(email, pwd)
    if not exito:
        flash(f"Error: {mensaje}", "danger")
        return render_template("pages/recuperar_contrasena.html")

    _emails_debe_cambiar.add(email.lower())
    ok_email, msg_email = enviar_contrasena_temporal(email, pwd)

    if ok_email:
        flash("Se envio una contrasena temporal a su correo.", "success")
    else:
        flash(f"Contrasena restablecida pero no se pudo enviar el correo: {msg_email}", "warning")

    return redirect(url_for("auth.login"))
