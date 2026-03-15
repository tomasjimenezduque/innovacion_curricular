# Frontend Flask - CRUD Facturas Tutorial

<p align="center">
  <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask">
  <img src="https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white" alt="Bootstrap">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Jinja2-B41717?style=for-the-badge&logo=jinja&logoColor=white" alt="Jinja2">
</p>

> **Proyecto Tutorial**: Frontend web desarrollado con Flask que consume la API REST de FastAPI para gestionar productos. Incluye una clase `ApiService` generica reutilizable y plantillas HTML comentadas para principiantes.

## Tabla de Contenidos

1. [Descripcion del Proyecto](#descripcion-del-proyecto)
2. [Arquitectura](#arquitectura)
3. [Tecnologias](#tecnologias)
4. [Prerrequisitos](#prerrequisitos)
5. [Instalacion](#instalacion)
6. [Ejecucion](#ejecucion)
7. [Estructura del Proyecto](#estructura-del-proyecto)
8. [Clase ApiService](#clase-apiservice)
9. [Como agregar una nueva tabla](#como-agregar-una-nueva-tabla)
10. [Notas tecnicas](#notas-tecnicas)

---

## Descripcion del Proyecto

Este proyecto es un **frontend web** que permite realizar operaciones CRUD (Crear, Leer, Actualizar, Eliminar) sobre productos a traves del navegador. Se comunica con una API REST desarrollada en FastAPI.

### Caracteristicas Principales

- **CRUD Completo visual**: Formularios y tablas para gestionar productos
- **Clase ApiService generica**: Reutilizable para cualquier tabla sin modificar
- **Plantillas con herencia**: Jinja2 con layout base y componentes
- **Diseño responsivo**: Bootstrap 5 + CSS personalizado con sidebar
- **Servidor rapido**: Waitress (multi-hilo) en vez del servidor de desarrollo de Flask
- **Codigo ultra-comentado**: Cada archivo explica conceptos desde cero (HTML, CSS, HTTP, Flask)

---

## Arquitectura

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  Navegador   │────→│    Flask     │────→│  ApiService  │────→│  API FastAPI │
│  (Usuario)   │     │  (routes/)   │     │ (services/)  │     │  (Backend)   │
│              │←────│              │←────│              │←────│              │
│  Ve HTML     │     │ Renderiza    │     │  Hace HTTP   │     │  Consulta    │
│              │     │ plantillas   │     │  requests    │     │  PostgreSQL  │
└──────────────┘     └──────────────┘     └──────────────┘     └──────────────┘
```

### Flujo de una peticion (Listar Productos)

1. Usuario visita `http://127.0.0.1:5200/producto`
2. Flask ejecuta `index()` en `routes/producto.py`
3. `index()` llama a `api.listar("producto")`
4. `ApiService` hace `GET http://127.0.0.1:8000/api/producto/`
5. La API responde con JSON
6. Flask renderiza `producto.html` con los datos
7. El navegador muestra la tabla de productos

---

## Tecnologias

| Categoria | Tecnologia | Descripcion |
|-----------|------------|-------------|
| **Framework** | Flask 3.1 | Framework web para renderizar HTML |
| **HTTP Client** | Requests 2.32 | Comunicacion con la API backend |
| **Servidor** | Waitress 3.0 | Servidor WSGI multi-hilo (rapido en Windows) |
| **Plantillas** | Jinja2 | Motor de templates con herencia |
| **Estilos** | Bootstrap 5.3 | Framework CSS responsivo (CDN) |
| **CSS** | app.css | Estilos personalizados (sidebar, layout) |

---

## Prerrequisitos

1. **Python 3.10+**
2. **API FastAPI corriendo** en `http://127.0.0.1:8000` (ver proyecto `apifacturas_fastapi_tutorial`)

---

## Instalacion

```bash
# 1. Navegar a la carpeta del proyecto
cd FrontFlask_Facturas_Tutorial

# 2. Crear entorno virtual
python -m venv venv

# 3. Activar entorno virtual
# Windows PowerShell:
venv\Scripts\Activate.ps1
# Windows CMD:
venv\Scripts\activate.bat
# Linux/Mac:
source venv/bin/activate

# 4. Instalar dependencias
pip install -r requirements.txt
```

---

## Ejecucion

### Terminal 1 — API Backend (FastAPI)

```bash
cd apifacturas_fastapi_tutorial
venv\Scripts\Activate.ps1
uvicorn main:app --reload
```
Verifica en: `http://127.0.0.1:8000/docs`

### Terminal 2 — Frontend (Flask)

```bash
cd FrontFlask_Facturas_Tutorial
venv\Scripts\Activate.ps1
python app.py
```

Abrir en el navegador: **http://127.0.0.1:5200**

### Paginas disponibles

| URL | Descripcion |
|-----|-------------|
| `http://127.0.0.1:5200/` | Pagina de inicio |
| `http://127.0.0.1:5200/producto` | CRUD de productos |
| `http://127.0.0.1:5200/producto?accion=nuevo` | Formulario de creacion |
| `http://127.0.0.1:5200/producto?accion=editar&clave=PR001` | Formulario de edicion |

---

## Estructura del Proyecto

```
FrontFlask_Facturas_Tutorial/
├── app.py                          # Punto de entrada (Waitress, puerto 5200)
├── config.py                       # URL de la API + clave secreta
├── requirements.txt                # Flask, requests, waitress
├── tutorial_frontend.md            # Tutorial detallado para principiantes
├── README.md                       # Este archivo
│
├── services/                       # Capa de comunicacion con la API
│   ├── __init__.py                 # Re-exporta ApiService
│   └── api_service.py             # Clase generica CRUD (GET/POST/PUT/DELETE)
│
├── routes/                         # Rutas/paginas (Blueprints Flask)
│   ├── __init__.py
│   ├── home.py                     # GET / → pagina de inicio
│   └── producto.py                 # CRUD /producto (listar, crear, editar, eliminar)
│
├── templates/                      # Plantillas HTML (Jinja2)
│   ├── layout/
│   │   └── base.html               # Layout maestro (sidebar + contenido + Bootstrap)
│   ├── components/
│   │   └── nav_menu.html           # Menu lateral de navegacion
│   └── pages/
│       ├── home.html               # Pagina de bienvenida
│       └── producto.html           # Tabla + formularios CRUD
│
└── static/                         # Archivos estaticos
    └── css/
        └── app.css                 # Estilos: sidebar, layout flexbox, responsive
```

---

## Clase ApiService

La clase `ApiService` en `services/api_service.py` es **generica**: funciona para cualquier tabla sin modificar.

### Metodos

| Metodo | HTTP | Ejemplo | Retorna |
|--------|------|---------|---------|
| `listar(tabla, limite)` | GET | `api.listar("producto", 5)` | `[{...}, ...]` o `[]` |
| `obtener(tabla, clave)` | GET | `api.obtener("producto", "PR001")` | `{...}` o `None` |
| `crear(tabla, datos)` | POST | `api.crear("producto", {...})` | `(True/False, "mensaje")` |
| `actualizar(tabla, clave, datos)` | PUT | `api.actualizar("producto", "PR001", {...})` | `(True/False, "mensaje")` |
| `eliminar(tabla, clave)` | DELETE | `api.eliminar("producto", "PR001")` | `(True/False, "mensaje")` |

### Uso rapido

```python
from services import ApiService

api = ApiService()

# Listar
productos = api.listar("producto")

# Crear
exito, msg = api.crear("producto", {
    "codigo": "PR100",
    "nombre": "Teclado",
    "stock": 10,
    "valorunitario": 50000
})

# Actualizar
exito, msg = api.actualizar("producto", "PR100", {
    "codigo": "PR100",
    "nombre": "Teclado Mecanico",
    "stock": 8,
    "valorunitario": 75000
})

# Eliminar
exito, msg = api.eliminar("producto", "PR100")
```

---

## Como agregar una nueva tabla

Si la API tiene un endpoint `/api/empresa/`, sigue estos 4 pasos:

### 1. Crear ruta: `routes/empresa.py`

```python
from flask import Blueprint, render_template, request, redirect, url_for, flash
from services import ApiService

empresa_bp = Blueprint("empresa", __name__)
api = ApiService()

@empresa_bp.route("/empresa")
def index():
    empresas = api.listar("empresa", limite=request.args.get("limite"))
    return render_template("pages/empresa.html", empresas=empresas)

@empresa_bp.route("/empresa/crear", methods=["POST"])
def crear():
    datos = {"codigo": request.form.get("codigo"), "nombre": request.form.get("nombre")}
    exito, mensaje = api.crear("empresa", datos)
    flash(mensaje, "success" if exito else "danger")
    return redirect(url_for("empresa.index"))
```

### 2. Crear plantilla: `templates/pages/empresa.html`

Copiar `producto.html` y adaptar campos.

### 3. Registrar en `app.py`

```python
from routes.empresa import empresa_bp
app.register_blueprint(empresa_bp)
```

### 4. Agregar al menu: `templates/components/nav_menu.html`

Agregar un nuevo link de navegacion.

---

## Notas tecnicas

### ¿Por que Waitress y no app.run()?

El servidor de desarrollo de Flask (`app.run()`) es **mono-hilo** y muy lento. Waitress es multi-hilo y responde mucho mas rapido, especialmente en Windows.

### ¿Por que 127.0.0.1 y no localhost?

En Windows, `localhost` puede causar delays de ~2 segundos por intento de resolucion DNS IPv6. Usar `127.0.0.1` directamente evita este problema.

### ¿Por que el frontend es lento en la primera carga?

Bootstrap se carga desde un CDN externo. La primera vez necesita descargarlo. Despues el navegador lo cachea y es instantaneo.

---

## Comandos Git

### Configuracion inicial (solo la primera vez)

```bash
# Ver si Git esta instalado
git --version

# Configurar tu nombre y correo (se guarda en cada commit)
git config --global user.name "Tu Nombre"
git config --global user.email "tu@correo.com"

# Inicializar el repositorio (crea la carpeta oculta .git)
git init

# Agregar todos los archivos al staging (area de preparacion)
git add .

# Crear el primer commit (guardar el estado actual)
git commit -m "Primer commit: Frontend Flask Facturas"
```

### Comandos del dia a dia

```bash
# Ver el estado actual (que archivos cambiaron, cuales estan pendientes)
git status

# Ver los cambios que hiciste en detalle (linea por linea)
git diff

# Agregar archivos especificos al staging
git add nombre_archivo.py

# Agregar TODOS los archivos modificados al staging
git add .

# Crear un commit (guardar cambios con un mensaje descriptivo)
git commit -m "Agregar pagina de empresa al frontend"

# Ver el historial de commits (los mas recientes primero)
git log --oneline

# Ver el historial con mas detalle
git log
```

### Subir a GitHub (repositorio remoto)

```bash
# Conectar tu repositorio local con GitHub (solo la primera vez)
git remote add origin https://github.com/tu-usuario/tu-repositorio.git

# Subir los commits al repositorio remoto
git push -u origin main

# Las siguientes veces, solo necesitas:
git push
```

### Comandos para resolver errores comunes

```bash
# ERROR: "fatal: not a git repository"
# SOLUCION: No estas en la carpeta del proyecto, o no has hecho git init
cd FrontFlask_Facturas_Tutorial
git init

# ERROR: "nothing to commit, working tree clean"
# SIGNIFICADO: No hay cambios pendientes. Todo ya esta guardado.
# No es un error, es informativo.

# ERROR: "Changes not staged for commit"
# SOLUCION: Modificaste archivos pero no los agregaste al staging
git add .
git commit -m "Tu mensaje"

# ERROR: "Your branch is ahead of 'origin/main' by X commits"
# SIGNIFICADO: Tienes commits locales que no has subido a GitHub
git push

# ERROR: "failed to push some refs" (al hacer git push)
# SOLUCION: Alguien mas subio cambios. Necesitas traerlos primero
git pull origin main
# Si hay conflictos, abre los archivos marcados, resuelve y luego:
git add .
git commit -m "Resolver conflictos de merge"
git push

# ERROR: "Permission denied (publickey)" (al hacer git push)
# SOLUCION: No tienes configurada la autenticacion con GitHub
# Opcion 1: Usar HTTPS con token personal
git remote set-url origin https://TOKEN@github.com/tu-usuario/tu-repo.git
# Opcion 2: Configurar SSH key (ver documentacion de GitHub)

# QUIERO DESHACER el ultimo commit (pero mantener los cambios)
git reset --soft HEAD~1

# QUIERO DESCARTAR todos los cambios locales (CUIDADO: pierdes todo)
git checkout .

# QUIERO VER que archivos estan siendo ignorados por .gitignore
git status --ignored

# QUIERO CREAR UNA RAMA nueva (para experimentar sin afectar main)
git checkout -b nombre-rama

# QUIERO VOLVER a la rama principal
git checkout main

# QUIERO VER todas las ramas
git branch -a
```

### Archivo .gitignore recomendado

Si no tienes un `.gitignore`, crea uno con este contenido:

```
# Entorno virtual (no se sube, cada persona lo crea con pip install)
venv/

# Cache de Python
__pycache__/
*.pyc

# IDE
.vscode/
.idea/
```

---

## Recursos

- [Documentacion de Flask](https://flask.palletsprojects.com/)
- [Documentacion de Jinja2](https://jinja.palletsprojects.com/)
- [Bootstrap 5](https://getbootstrap.com/docs/5.3/)
- [Waitress](https://docs.pylonsproject.org/projects/waitress/)
- [tutorial_frontend.md](tutorial_frontend.md) — Tutorial paso a paso para principiantes

---

<p align="center">
  <strong>Desarrollado por:</strong><br>
  Carlos Arturo Castro Castro<br>
  Claude Code
</p>
