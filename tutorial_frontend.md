# Tutorial: Frontend Flask para API de Facturas

## ¿Qué vamos a construir?

Una **aplicación web** (frontend) que permite gestionar productos a través de una interfaz visual en el navegador. Esta aplicación se comunica con una **API REST** (backend en FastAPI) para realizar operaciones **CRUD**:

- **C**reate (Crear) → Agregar nuevos productos
- **R**ead (Leer) → Ver la lista de productos
- **U**pdate (Actualizar) → Modificar productos existentes
- **D**elete (Eliminar) → Borrar productos

---

## Antes de empezar: Conceptos que debes conocer

### ¿Qué es un Frontend?
Es la parte de una aplicación que el **usuario ve y toca**: botones, formularios, tablas, menús. En nuestro caso, son páginas HTML que se ven en el navegador.

### ¿Qué es un Backend (API)?
Es la parte que el usuario **NO ve**. Se encarga de la lógica, la base de datos, y responder peticiones. Nuestra API FastAPI es el backend.

### ¿Qué es Flask?
Flask es un **framework web** de Python. Un framework es como un "kit de herramientas" que te da funciones ya hechas para crear aplicaciones web sin empezar desde cero.

### ¿Qué es HTML?
HTML (HyperText Markup Language) es el lenguaje que define la **estructura** de una página web. Usa "etiquetas" como:
- `<p>` → un párrafo de texto
- `<button>` → un botón
- `<table>` → una tabla
- `<input>` → un campo donde el usuario escribe
- `<form>` → un formulario (agrupa varios inputs)

### ¿Qué es CSS?
CSS (Cascading Style Sheets) controla la **apariencia** del HTML: colores, tamaños, posiciones, fuentes, etc.

### ¿Qué es Bootstrap?
Bootstrap es una **librería CSS** creada por Twitter. Nos da estilos bonitos "gratis": botones con colores, tablas elegantes, formularios estilizados, diseño responsivo (que se adapta a celulares). Solo agregamos clases CSS como `class="btn btn-primary"` y Bootstrap se encarga del resto.

---

## Estructura del proyecto

```
FrontFlask_Facturas_Tutorial/
│
├── app.py                      ← Punto de entrada (ejecutas este archivo)
├── config.py                   ← Configuración (URL de la API, clave secreta)
├── requirements.txt            ← Dependencias (Flask y requests)
│
├── services/                   ← Capa de servicios (comunicación con la API)
│   ├── __init__.py             ← Marca como paquete Python + re-exporta
│   └── api_service.py          ← Clase ApiService (CRUD genérico)
│
├── routes/                     ← Rutas/páginas de la aplicación
│   ├── __init__.py             ← Marca como paquete Python
│   ├── home.py                 ← Ruta: página de inicio (/)
│   └── producto.py             ← Rutas: CRUD de productos (/producto)
│
├── templates/                  ← Plantillas HTML (lo que ve el usuario)
│   ├── layout/
│   │   └── base.html           ← Plantilla base (menú, estilos, estructura)
│   ├── components/
│   │   └── nav_menu.html       ← Componente: menú de navegación lateral
│   └── pages/
│       ├── home.html           ← Página: Inicio
│       └── producto.html       ← Página: CRUD de Productos
│
├── static/                     ← Archivos estáticos (CSS, JS, imágenes)
│   └── css/
│       └── app.css             ← Estilos personalizados
│
└── tutorial_frontend.md        ← Este archivo que estás leyendo
```

### ¿Por qué está organizado así?

| Carpeta     | Responsabilidad                                     |
|-------------|-----------------------------------------------------|
| `services/` | Hablar con la API (peticiones HTTP)                 |
| `routes/`   | Manejar las URLs y la lógica de cada página         |
| `templates/`| Definir cómo se ve cada página (HTML)               |
| `static/`   | Archivos que no cambian (CSS, imágenes)             |

Esta separación se llama **Separación de Responsabilidades**: cada carpeta tiene UN trabajo. Si algo falla en la comunicación con la API, sabes que está en `services/`. Si algo se ve mal, miras en `templates/` o `static/css/`.

---

## Paso 1: Crear el entorno virtual e instalar dependencias

```bash
# Navegar a la carpeta del proyecto
cd FrontFlask_Facturas_Tutorial

# Crear entorno virtual (una "burbuja" aislada para instalar librerías)
python -m venv venv

# Activar el entorno virtual
# En Windows:
venv\Scripts\activate
# En Mac/Linux:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### ¿Qué es un entorno virtual?
Imagina que cada proyecto tiene su propia "caja de herramientas". Si el Proyecto A necesita Flask 2.0 y el Proyecto B necesita Flask 3.0, sin entornos virtuales habría conflicto. Con `venv`, cada proyecto tiene sus propias versiones de librerías sin afectar al otro.

---

## Paso 2: Verificar que la API esté corriendo

Antes de iniciar el frontend, la API FastAPI debe estar encendida:

```bash
# En OTRA terminal, en la carpeta de la API:
cd apifacturas_fastapi_tutorial
venv\Scripts\activate
uvicorn main:app --reload
```

Verifica en tu navegador: http://localhost:8000/docs (debe mostrar la documentación de la API).

---

## Paso 3: Ejecutar el frontend

```bash
# En la carpeta del frontend:
cd FrontFlask_Facturas_Tutorial
venv\Scripts\activate
python app.py
```

Abre tu navegador en: **http://localhost:5100**

---

## Cómo funciona: El flujo completo

### Ejemplo: El usuario quiere ver la lista de productos

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  Navegador   │────→│  Flask       │────→│  ApiService   │────→│  API FastAPI │
│  (Usuario)   │     │  (routes/)   │     │  (services/)  │     │  (Backend)   │
│              │     │              │     │              │     │              │
│ Escribe URL: │     │ Ejecuta      │     │ Hace GET a:  │     │ Consulta     │
│ /producto    │     │ index() en   │     │ localhost:8000│     │ PostgreSQL   │
│              │     │ producto.py  │     │ /api/producto │     │ y responde   │
│              │←────│              │←────│              │←────│ con JSON     │
│ Ve la tabla  │     │ Renderiza    │     │ Retorna lista│     │              │
│ de productos │     │ producto.html│     │ de productos │     │              │
└──────────────┘     └──────────────┘     └──────────────┘     └──────────────┘
```

### Ejemplo: El usuario crea un nuevo producto

```
1. Usuario llena el formulario y clic en "Guardar"
2. Navegador envía POST /producto/crear con los datos
3. Flask ejecuta crear() en routes/producto.py
4. crear() extrae datos del formulario (request.form)
5. crear() llama a api.crear("producto", datos)
6. ApiService envía POST http://localhost:8000/api/producto/ con JSON
7. API FastAPI guarda en PostgreSQL y responde {"mensaje": "..."}
8. ApiService retorna (True, "Producto creado exitosamente.")
9. crear() guarda el mensaje con flash() y redirige a /producto
10. Navegador carga /producto (GET) y muestra tabla + mensaje verde
```

---

## La clase ApiService explicada

`ApiService` es el corazón de la comunicación con la API. Es una clase **genérica** (funciona para cualquier tabla).

### ¿Por qué es importante?

Sin ApiService, cada ruta tendría que escribir su propio código de peticiones HTTP:

```python
# SIN ApiService (código repetido en CADA ruta):
import requests
respuesta = requests.get("http://localhost:8000/api/producto/")
datos = respuesta.json()
productos = datos.get("datos", [])
```

Con ApiService:

```python
# CON ApiService (una sola línea):
productos = api.listar("producto")
```

### Métodos disponibles

| Método                               | ¿Qué hace?                           | HTTP   |
|--------------------------------------|---------------------------------------|--------|
| `api.listar("producto")`             | Obtener todos los productos           | GET    |
| `api.listar("producto", limite=5)`   | Obtener máximo 5 productos            | GET    |
| `api.obtener("producto", "PR001")`   | Obtener UN producto por su código     | GET    |
| `api.crear("producto", datos)`       | Crear un nuevo producto               | POST   |
| `api.actualizar("producto", "PR001", datos)` | Actualizar producto PR001    | PUT    |
| `api.eliminar("producto", "PR001")`  | Eliminar producto PR001               | DELETE |

### ¿Qué retorna cada método?

- **listar()** → `[{...}, {...}, ...]` (lista de diccionarios) o `[]` si hay error
- **obtener()** → `{...}` (un diccionario) o `None` si no existe
- **crear()** → `(True, "mensaje")` o `(False, "error")`
- **actualizar()** → `(True, "mensaje")` o `(False, "error")`
- **eliminar()** → `(True, "mensaje")` o `(False, "error")`

---

## Herencia de plantillas (Jinja2)

Las plantillas usan **herencia**, como las clases en programación:

```
base.html (padre)
├── define: menú lateral, Bootstrap, estilos, estructura general
├── define bloques vacíos: titulo, encabezado, contenido
│
├── home.html (hijo)
│   └── rellena: titulo="Inicio", contenido=bienvenida
│
└── producto.html (hijo)
    └── rellena: titulo="Productos", contenido=tabla+formularios
```

`base.html` define el "esqueleto" con bloques (`{% block nombre %}`).
Las páginas hijas "heredan" con `{% extends "layout/base.html" %}` y solo definen los bloques que necesitan cambiar.

---

## Cómo agregar una nueva tabla (ejemplo: Empresa)

Si la API tiene un endpoint `/api/empresa/`, puedes agregar la página así:

### 1. Crear la ruta (`routes/empresa.py`)

```python
from flask import Blueprint, render_template, request, redirect, url_for, flash
from services import ApiService

empresa_bp = Blueprint("empresa", __name__)
api = ApiService()

@empresa_bp.route("/empresa")
def index():
    limite = request.args.get("limite")
    accion = request.args.get("accion")
    clave = request.args.get("clave")

    empresas = api.listar("empresa", limite=limite)

    empresa_editar = None
    if accion == "editar" and clave:
        empresa_editar = api.obtener("empresa", clave)

    return render_template("pages/empresa.html",
        empresas=empresas, accion=accion,
        empresa_editar=empresa_editar, limite=limite)

@empresa_bp.route("/empresa/crear", methods=["POST"])
def crear():
    datos = {
        "codigo": request.form.get("codigo"),
        "nombre": request.form.get("nombre"),
    }
    exito, mensaje = api.crear("empresa", datos)
    flash(mensaje, "success" if exito else "danger")
    return redirect(url_for("empresa.index"))

# ... actualizar y eliminar (mismo patrón que producto.py)
```

### 2. Crear la plantilla (`templates/pages/empresa.html`)

Copia `producto.html` y cambia:
- `productos` → `empresas`
- `producto_editar` → `empresa_editar`
- Los campos del formulario y la tabla

### 3. Registrar en `app.py`

```python
from routes.empresa import empresa_bp
app.register_blueprint(empresa_bp)
```

### 4. Agregar al menú (`templates/components/nav_menu.html`)

```html
<a class="nav-link nav-item
    {% if '/empresa' in request.path %}active{% endif %}"
    href="{{ url_for('empresa.index') }}">
    <span class="bi-list-nested-nav-menu"></span>
    Empresa
</a>
```

---

## Glosario rápido

| Término          | Significado                                                      |
|------------------|------------------------------------------------------------------|
| **API**          | Interfaz para que programas se comuniquen entre sí               |
| **REST**         | Estilo de diseño de APIs usando URLs y métodos HTTP              |
| **HTTP**         | Protocolo de comunicación web (GET, POST, PUT, DELETE)           |
| **JSON**         | Formato de texto para intercambiar datos: `{"clave": "valor"}`  |
| **Blueprint**    | Módulo de Flask que agrupa rutas relacionadas                    |
| **Jinja2**       | Motor de plantillas: permite usar Python dentro de HTML          |
| **Template**     | Plantilla HTML con variables y lógica (`{{ }}`, `{% %}`)         |
| **Flash**        | Mensaje temporal que se muestra una vez tras una acción          |
| **Render**       | Convertir una plantilla (con variables) en HTML puro             |
| **Redirect**     | Enviar al usuario a otra URL automáticamente                     |
| **CDN**          | Servidor externo que hospeda archivos (como Bootstrap)           |
| **Flexbox**      | Sistema CSS para organizar elementos en filas/columnas           |
| **Responsive**   | Diseño que se adapta a diferentes tamaños de pantalla            |
| **CRUD**         | Create, Read, Update, Delete (las 4 operaciones de datos)       |
