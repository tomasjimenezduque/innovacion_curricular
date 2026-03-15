"""
api_service.py — Clase genérica para comunicarse con la API backend.

╔══════════════════════════════════════════════════════════════════╗
║  CONCEPTO CLAVE: ¿Qué es un "servicio" en programación?        ║
╠══════════════════════════════════════════════════════════════════╣
║  Un servicio es una clase que se encarga de UNA responsabilidad ║
║  específica. En este caso: hablar con la API.                   ║
║                                                                  ║
║  Sin ApiService, cada ruta tendría que escribir su propio       ║
║  código de requests.get(), requests.post(), manejar errores...  ║
║  Eso sería MUCHO código repetido.                               ║
║                                                                  ║
║  Con ApiService, las rutas simplemente hacen:                   ║
║    api = ApiService()                                           ║
║    productos = api.listar("producto")                           ║
║  Y ApiService se encarga del resto.                             ║
║                                                                  ║
║  Es como usar un control remoto: tú solo presionas "Listar"    ║
║  y el control se encarga de enviar la señal correcta.           ║
╚══════════════════════════════════════════════════════════════════╝

────────────────────────────────────────────────────────────────────
PATRÓN: Esta clase es GENÉRICA.
────────────────────────────────────────────────────────────────────
"Genérica" significa que funciona para CUALQUIER tabla, no solo
para productos. Si mañana agregas una tabla "empresa", solo haces:
    api.listar("empresa")
    api.crear("empresa", datos)
No necesitas crear una nueva clase ni modificar esta.

El truco es que la URL de la API sigue un patrón predecible:
    /api/producto/      → tabla "producto"
    /api/empresa/       → tabla "empresa"
    /api/{lo-que-sea}/  → tabla "{lo-que-sea}"
────────────────────────────────────────────────────────────────────
"""

# ─── Imports ─────────────────────────────────────────────────

import requests
# "requests" es la librería que nos permite hacer peticiones HTTP.
# HTTP es el protocolo que usan los navegadores para comunicarse
# con los servidores. Las peticiones más comunes son:
#
#   GET    → Pedir datos (como abrir una página web)
#   POST   → Enviar datos nuevos (como llenar un formulario)
#   PUT    → Actualizar datos existentes
#   DELETE → Borrar datos
#
# requests nos da métodos para cada una:
#   requests.get(url)      → petición GET
#   requests.post(url)     → petición POST
#   requests.put(url)      → petición PUT
#   requests.delete(url)   → petición DELETE

from config import API_BASE_URL
# Importa la URL base de la API desde config.py.
# Ejemplo: "http://localhost:8000"


class ApiService:
    """
    Servicio genérico para operaciones CRUD contra la API FastAPI.

    CRUD = Create (Crear), Read (Leer), Update (Actualizar), Delete (Eliminar).
    Son las 4 operaciones básicas que puedes hacer con datos.

    Métodos disponibles:
    ─────────────────────────────────────────────────────────────
    │ Método       │ HTTP   │ ¿Qué hace?                       │
    ─────────────────────────────────────────────────────────────
    │ listar()     │ GET    │ Obtener todos los registros       │
    │ obtener()    │ GET    │ Obtener UN registro por su clave  │
    │ crear()      │ POST   │ Crear un nuevo registro           │
    │ actualizar() │ PUT    │ Modificar un registro existente   │
    │ eliminar()   │ DELETE │ Borrar un registro                │
    ─────────────────────────────────────────────────────────────

    Ejemplo de uso:
        api = ApiService()
        productos = api.listar("producto", limite=5)
        exito, mensaje = api.crear("producto", {"codigo": "PR100", ...})
    """

    def __init__(self):
        """
        Constructor: se ejecuta al crear la instancia → ApiService().

        Guarda la URL base para usarla en todos los métodos.
        self.base_url será algo como: "http://localhost:8000/api"
        """
        # Construye la URL base agregando "/api" al final.
        # Resultado: "http://localhost:8000/api"
        self.base_url = f"{API_BASE_URL}/api"

    # ═══════════════════════════════════════════════════════════
    #  LISTAR — Obtener todos los registros de una tabla
    # ═══════════════════════════════════════════════════════════
    def listar(self, tabla, limite=None):
        """
        Obtiene una lista de registros de la API.

        Parámetros:
        ───────────
        tabla  (str): Nombre de la tabla. Ejemplo: "producto"
        limite (int): Cantidad máxima de resultados. None = todos.

        Retorna:
        ────────
        list: Lista de diccionarios. Cada diccionario es un registro.
              Ejemplo: [{"codigo": "PR001", "nombre": "Laptop", ...}, ...]
              Si hay error: retorna lista vacía []

        ¿Cómo funciona?
        ────────────────
        1. Arma la URL: http://localhost:8000/api/producto/
        2. Si hay límite, agrega: ?limite=5
        3. Hace GET a esa URL
        4. La API responde con JSON: {"datos": [...], "total": 10}
        5. Extrae la lista de "datos" y la retorna
        """
        # ─── Paso 1: Construir la URL ────────────────────────
        url = f"{self.base_url}/{tabla}/"
        # Si tabla = "producto", url = "http://localhost:8000/api/producto/"

        # ─── Paso 2: Agregar parámetros de consulta ──────────
        # "params" es un diccionario con los parámetros de la URL.
        # requests los convierte a: ?limite=5
        # Si limite es None, enviamos diccionario vacío (sin parámetros).
        params = {}
        if limite:
            params["limite"] = limite

        # ─── Paso 3: Hacer la petición GET ────────────────────
        try:
            respuesta = requests.get(url, params=params)
            # requests.get() envía una petición HTTP GET.
            # "respuesta" es un objeto Response que contiene:
            #   .status_code → código HTTP (200 = OK, 404 = no encontrado)
            #   .json()      → convierte la respuesta JSON a diccionario Python
            #   .text        → respuesta como texto plano

            # ─── Paso 4: Extraer los datos ────────────────────
            datos = respuesta.json()
            # Convierte el JSON de la API a un diccionario Python.
            # Ejemplo de lo que retorna la API:
            # {
            #     "tabla": "producto",
            #     "total": 3,
            #     "datos": [
            #         {"codigo": "PR001", "nombre": "Laptop", ...},
            #         {"codigo": "PR002", "nombre": "Mouse", ...},
            #     ]
            # }

            return datos.get("datos", [])
            # .get("datos", []) busca la clave "datos" en el diccionario.
            # Si no existe (por algún error), retorna lista vacía [].
            # Es más seguro que datos["datos"] que lanzaría un error.

        except requests.RequestException as e:
            # ─── Manejo de errores ────────────────────────────
            # requests.RequestException atrapa TODOS los errores de red:
            #   - La API no está encendida (ConnectionError)
            #   - La URL está mal (InvalidURL)
            #   - La conexión tardó mucho (Timeout)
            #
            # "as e" guarda el error en la variable "e" para imprimirlo.
            print(f"[ERROR] No se pudo conectar a la API: {e}")
            return []
            # Retornamos lista vacía para que la página se muestre
            # (sin datos, pero sin crashear).

    # ═══════════════════════════════════════════════════════════
    #  OBTENER — Obtener UN solo registro por su clave
    # ═══════════════════════════════════════════════════════════
    def obtener(self, tabla, valor_clave):
        """
        Obtiene un único registro de la API usando su clave primaria.

        Parámetros:
        ───────────
        tabla       (str): Nombre de la tabla. Ejemplo: "producto"
        valor_clave (str): Valor de la clave primaria. Ejemplo: "PR001"

        Retorna:
        ────────
        dict: Diccionario con los datos del registro.
              Ejemplo: {"codigo": "PR001", "nombre": "Laptop", ...}
              Si hay error o no existe: retorna None

        ¿Cómo funciona?
        ────────────────
        1. Arma la URL: http://localhost:8000/api/producto/PR001
        2. Hace GET a esa URL
        3. La API responde con: {"datos": [{"codigo": "PR001", ...}]}
        4. Extrae el primer (y único) elemento de "datos"
        """
        url = f"{self.base_url}/{tabla}/{valor_clave}"

        try:
            respuesta = requests.get(url)
            if respuesta.status_code == 200:
                datos = respuesta.json()
                lista = datos.get("datos", [])
                # La API siempre retorna una LISTA dentro de "datos",
                # incluso cuando es un solo registro: [{"codigo": "PR001"}]
                if lista:
                    return lista[0]
                    # lista[0] = el primer (y único) elemento de la lista.
            return None
            # Si el status code no es 200 (ej: 404 = no encontrado),
            # retornamos None para indicar que no se encontró.

        except requests.RequestException as e:
            print(f"[ERROR] No se pudo obtener registro: {e}")
            return None

    # ═══════════════════════════════════════════════════════════
    #  CREAR — Crear un nuevo registro
    # ═══════════════════════════════════════════════════════════
    def crear(self, tabla, datos):
        """
        Envía datos nuevos a la API para crear un registro.

        Parámetros:
        ───────────
        tabla (str):  Nombre de la tabla. Ejemplo: "producto"
        datos (dict): Diccionario con los campos del nuevo registro.
                      Ejemplo: {"codigo": "PR100", "nombre": "Teclado",
                                "stock": 10, "valorunitario": 50000}

        Retorna:
        ────────
        tuple: (éxito, mensaje)
            éxito   (bool): True si se creó correctamente, False si falló.
            mensaje (str):  Texto descriptivo del resultado.
            Ejemplo éxito: (True, "Producto creado exitosamente.")
            Ejemplo fallo: (False, "Error: el código ya existe")

        ¿Cómo funciona?
        ────────────────
        1. Arma la URL: http://localhost:8000/api/producto/
        2. Convierte "datos" a JSON y lo envía con POST
        3. La API intenta crear el registro en la base de datos
        4. La API responde con éxito o error
        5. Extraemos el mensaje y lo retornamos
        """
        url = f"{self.base_url}/{tabla}/"

        try:
            respuesta = requests.post(url, json=datos)
            # requests.post(url, json=datos) hace una petición POST.
            # El parámetro "json=datos" hace DOS cosas:
            #   1. Convierte el diccionario Python a texto JSON
            #   2. Agrega el encabezado Content-Type: application/json
            # Así la API sabe que le estamos enviando datos en formato JSON.

            cuerpo = respuesta.json()
            # Convertimos la respuesta de la API a diccionario.

            if respuesta.status_code in (200, 201):
                # 200 = OK, 201 = Created (recurso creado)
                mensaje = cuerpo.get("mensaje", "Registro creado.")
                return (True, mensaje)
            else:
                # Si hubo un error (ej: código duplicado, campo faltante)
                # La API puede retornar el error en "detail" o "mensaje"
                detalle = cuerpo.get("detail", cuerpo.get("mensaje", ""))
                if isinstance(detalle, dict):
                    mensaje = detalle.get("mensaje", str(detalle))
                else:
                    mensaje = str(detalle)
                return (False, f"Error: {mensaje}")

        except requests.RequestException as e:
            return (False, f"Error de conexión: {e}")

    # ═══════════════════════════════════════════════════════════
    #  ACTUALIZAR — Modificar un registro existente
    # ═══════════════════════════════════════════════════════════
    def actualizar(self, tabla, valor_clave, datos):
        """
        Envía datos modificados a la API para actualizar un registro.

        Parámetros:
        ───────────
        tabla       (str):  Nombre de la tabla. Ejemplo: "producto"
        valor_clave (str):  Clave primaria del registro a modificar.
                            Ejemplo: "PR001"
        datos       (dict): Diccionario con TODOS los campos del registro
                            (incluyendo los que no cambiaron).

        Retorna:
        ────────
        tuple: (éxito, mensaje) — igual que crear()

        ¿Cómo funciona?
        ────────────────
        1. Arma la URL: http://localhost:8000/api/producto/PR001
        2. Convierte "datos" a JSON y lo envía con PUT
        3. La API busca el registro PR001 y lo actualiza
        4. Retorna éxito o error
        """
        url = f"{self.base_url}/{tabla}/{valor_clave}"

        try:
            respuesta = requests.put(url, json=datos)
            # requests.put() es igual que .post() pero usa el método PUT.
            # PUT se usa por convención para ACTUALIZAR recursos existentes.
            # POST se usa para CREAR recursos nuevos.

            cuerpo = respuesta.json()

            if respuesta.status_code == 200:
                mensaje = cuerpo.get("mensaje", "Registro actualizado.")
                return (True, mensaje)
            else:
                detalle = cuerpo.get("detail", cuerpo.get("mensaje", ""))
                if isinstance(detalle, dict):
                    mensaje = detalle.get("mensaje", str(detalle))
                else:
                    mensaje = str(detalle)
                return (False, f"Error: {mensaje}")

        except requests.RequestException as e:
            return (False, f"Error de conexión: {e}")

    # ═══════════════════════════════════════════════════════════
    #  ELIMINAR — Borrar un registro
    # ═══════════════════════════════════════════════════════════
    def eliminar(self, tabla, valor_clave):
        """
        Pide a la API que elimine un registro.

        Parámetros:
        ───────────
        tabla       (str): Nombre de la tabla. Ejemplo: "producto"
        valor_clave (str): Clave primaria del registro a borrar.
                           Ejemplo: "PR001"

        Retorna:
        ────────
        tuple: (éxito, mensaje) — igual que crear()

        ¿Cómo funciona?
        ────────────────
        1. Arma la URL: http://localhost:8000/api/producto/PR001
        2. Hace una petición DELETE a esa URL
        3. La API busca PR001 y lo borra de la base de datos
        4. Retorna éxito o error
        """
        url = f"{self.base_url}/{tabla}/{valor_clave}"

        try:
            respuesta = requests.delete(url)
            # requests.delete() envía una petición HTTP DELETE.
            # Es la operación más "peligrosa" porque borra datos.
            # Por eso en la interfaz siempre pedimos confirmación al usuario.

            cuerpo = respuesta.json()

            if respuesta.status_code == 200:
                mensaje = cuerpo.get("mensaje", "Registro eliminado.")
                return (True, mensaje)
            else:
                detalle = cuerpo.get("detail", cuerpo.get("mensaje", ""))
                if isinstance(detalle, dict):
                    mensaje = detalle.get("mensaje", str(detalle))
                else:
                    mensaje = str(detalle)
                return (False, f"Error: {mensaje}")

        except requests.RequestException as e:
            return (False, f"Error de conexión: {e}")
