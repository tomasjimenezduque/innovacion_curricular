"""
factura.py - Blueprint CRUD para Facturas usando la API generica FastAPI.

══════════════════════════════════════════════════════════════════════════
IMPORTANTE: LIMITACIONES DEL ENFOQUE SIN STORED PROCEDURES
══════════════════════════════════════════════════════════════════════════

Este archivo implementa el CRUD de facturas usando SOLO el endpoint
generico de la API (GET/POST/PUT/DELETE /api/{tabla}/{clave}/{valor}).

Esto tiene DESVENTAJAS frente al enfoque con Stored Procedures (SPs):

  1. MULTIPLES LLAMADAS HTTP: Para listar facturas con sus productos,
     clientes y vendedores se necesitan 5 llamadas a la API:
       - GET /api/factura
       - GET /api/productosporfactura
       - GET /api/cliente
       - GET /api/vendedor
       - GET /api/persona
     Con un SP seria UNA SOLA llamada:
       - POST /api/procedimientos/ejecutarsp  (sp_listar_facturas...)

  2. JOINS EN PYTHON: Los "joins" entre tablas (factura + cliente + persona)
     se hacen en memoria (Python) en vez de en la base de datos (SQL).
     Esto es MAS LENTO y consume MAS MEMORIA en el servidor web.
     Con SPs, los JOINs se hacen en la BD (mucho mas eficiente).

  3. SIN TRANSACCIONES: Al crear una factura con productos, se hacen
     llamadas separadas (crear factura + crear cada producto). Si falla
     a mitad de camino, quedan datos inconsistentes (factura sin productos).
     Con SPs, todo se ejecuta dentro de una TRANSACCION (todo o nada).

  4. TRAER TABLAS COMPLETAS: Para obtener UNA factura, se traen TODAS
     las facturas y se filtra en Python. Con SPs, la BD filtra por PK.

  RECOMENDACION: En un entorno de produccion, usar Stored Procedures
  para operaciones maestro-detalle como facturas. Este enfoque es
  solo para fines didacticos cuando no se dispone de SPs.
══════════════════════════════════════════════════════════════════════════

Tablas involucradas:
  - factura:              numero (PK), fkidcliente, fkidvendedor, fecha, total
  - productosporfactura:  fknumerofactura (FK), fkcodigoproducto (FK), cantidad
  - cliente:              id (PK), fkcodpersona (FK), credito
  - vendedor:             id (PK), fkcodpersona (FK), carnet
  - persona:              codigo (PK), nombre
  - producto:             codigo (PK), nombre, stock, valorunitario
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.api_service import ApiService

bp = Blueprint('factura', __name__)
api = ApiService()


# ══════════════════════════════════════════════════════════════════════
# FUNCION AUXILIAR: Enriquecer facturas con datos relacionados
# ══════════════════════════════════════════════════════════════════════
# Esta funcion hace lo que un SP haria en UNA sola consulta SQL:
#   SELECT f.*, c.nombre AS nombre_cliente, v.nombre AS nombre_vendedor,
#          p.codigo, p.nombre, pf.cantidad, p.valorunitario
#   FROM factura f
#   JOIN cliente c ON f.fkidcliente = c.id
#   JOIN vendedor v ON f.fkidvendedor = v.id
#   JOIN persona pc ON c.fkcodpersona = pc.codigo
#   JOIN persona pv ON v.fkcodpersona = pv.codigo
#   LEFT JOIN productosporfactura pf ON f.numero = pf.fknumerofactura
#   LEFT JOIN producto p ON pf.fkcodigoproducto = p.codigo
#
# Pero como no tenemos SPs, hacemos 5 GETs y "joinamos" en Python.
# ══════════════════════════════════════════════════════════════════════

def _enriquecer_facturas(facturas):
    """
    Agrega nombre_cliente, nombre_vendedor y lista de productos
    a cada factura. Requiere 5 llamadas HTTP a la API.

    Con SPs esto seria UNA SOLA llamada:
      api.ejecutar_sp("sp_listar_facturas_y_productosporfactura")

    Parametros:
        facturas (list): Lista de diccionarios con datos de factura.
    Retorna:
        list: Las mismas facturas enriquecidas con datos relacionados.
    """
    if not facturas:
        return []

    # ─── 5 llamadas HTTP (con SPs seria 1 sola) ─────────────────
    clientes = api.listar('cliente')
    vendedores = api.listar('vendedor')
    personas = api.listar('persona')
    productos_catalogo = api.listar('producto')
    productos_por_factura = api.listar('productosporfactura')

    # ─── Construir mapas para "join" en Python ───────────────────
    # Equivalente a: JOIN persona ON cliente.fkcodpersona = persona.codigo
    mapa_personas = {p.get('codigo'): p.get('nombre', '') for p in personas}

    # Equivalente a: JOIN cliente ON factura.fkidcliente = cliente.id
    mapa_clientes = {}
    for cli in clientes:
        nombre = mapa_personas.get(cli.get('fkcodpersona'), 'Sin nombre')
        mapa_clientes[cli.get('id')] = nombre

    # Equivalente a: JOIN vendedor ON factura.fkidvendedor = vendedor.id
    mapa_vendedores = {}
    for ven in vendedores:
        nombre = mapa_personas.get(ven.get('fkcodpersona'), 'Sin nombre')
        mapa_vendedores[ven.get('id')] = nombre

    # Mapa de productos para obtener nombre y precio
    mapa_productos = {p.get('codigo'): p for p in productos_catalogo}

    # ─── Enriquecer cada factura ─────────────────────────────────
    for fac in facturas:
        # Agregar nombres (equivalente a SELECT con JOINs)
        fac['nombre_cliente'] = mapa_clientes.get(fac.get('fkidcliente'), 'Sin cliente')
        fac['nombre_vendedor'] = mapa_vendedores.get(fac.get('fkidvendedor'), 'Sin vendedor')

        # Filtrar productos de esta factura
        # Equivalente a: WHERE productosporfactura.fknumerofactura = factura.numero
        prods_fac = [
            pf for pf in productos_por_factura
            if pf.get('fknumerofactura') == fac.get('numero')
        ]

        # Construir detalle de productos con subtotal calculado
        productos_detalle = []
        for pf in prods_fac:
            prod_info = mapa_productos.get(pf.get('fkcodigoproducto'), {})
            cantidad = pf.get('cantidad', 0)
            valor_unit = float(prod_info.get('valorunitario', 0))
            productos_detalle.append({
                'codigo_producto': pf.get('fkcodigoproducto'),
                'nombre_producto': prod_info.get('nombre', ''),
                'cantidad': cantidad,
                'valorunitario': valor_unit,
                'subtotal': cantidad * valor_unit
                # Con SPs, el subtotal lo calcula la BD directamente
            })
        fac['productos'] = productos_detalle

    return facturas


# ══════════════════════════════════════════════════════════════════════
# LISTAR: GET /factura
# ══════════════════════════════════════════════════════════════════════
# Con SPs seria:
#   api.ejecutar_sp("sp_listar_facturas_y_productosporfactura")
# Sin SPs: listar + enriquecer con 5 GETs adicionales
# ══════════════════════════════════════════════════════════════════════

@bp.route('/factura')
def index():
    facturas = api.listar('factura')
    facturas = _enriquecer_facturas(facturas)
    return render_template('pages/factura.html', facturas=facturas, vista='listar')


# ══════════════════════════════════════════════════════════════════════
# VER DETALLE: GET /factura/ver/<numero>
# ══════════════════════════════════════════════════════════════════════
# Con SPs seria:
#   api.ejecutar_sp("sp_consultar_factura_y_productosporfactura",
#                    {"p_numero": numero})
# Sin SPs: traer TODAS las facturas, filtrar en Python, luego enriquecer
# ══════════════════════════════════════════════════════════════════════

@bp.route('/factura/ver/<int:numero>')
def ver(numero):
    # Sin SPs, traemos todas y filtramos en Python (ineficiente)
    facturas = api.listar('factura')
    factura = next((f for f in facturas if f.get('numero') == numero), None)

    if factura:
        _enriquecer_facturas([factura])

    return render_template('pages/factura.html', factura=factura, vista='ver')


# ══════════════════════════════════════════════════════════════════════
# FORMULARIO NUEVA FACTURA: GET /factura/nueva
# ══════════════════════════════════════════════════════════════════════
# Carga los datos necesarios para los selects del formulario:
# clientes, vendedores y productos disponibles.
# ══════════════════════════════════════════════════════════════════════

@bp.route('/factura/nueva')
def nueva():
    # Cargar datos para los selects del formulario
    clientes = api.listar('cliente')
    vendedores = api.listar('vendedor')
    personas = api.listar('persona')
    productos = api.listar('producto')

    # Agregar nombre de persona a clientes y vendedores
    # (la tabla cliente/vendedor solo tiene fkcodpersona, no el nombre)
    mapa_personas = {p.get('codigo'): p.get('nombre', '') for p in personas}
    for cli in clientes:
        cli['nombre'] = mapa_personas.get(cli.get('fkcodpersona'), 'Sin nombre')
    for ven in vendedores:
        ven['nombre'] = mapa_personas.get(ven.get('fkcodpersona'), 'Sin nombre')

    return render_template('pages/factura.html',
        vista='formulario', editando=False,
        clientes=clientes, vendedores=vendedores,
        productos_disponibles=productos
    )


# ══════════════════════════════════════════════════════════════════════
# CREAR FACTURA: POST /factura/crear
# ══════════════════════════════════════════════════════════════════════
# Con SPs seria UNA SOLA llamada con transaccion:
#   api.ejecutar_sp("sp_insertar_factura_y_productosporfactura", {
#       "p_fkidcliente": ..., "p_fkidvendedor": ...,
#       "p_productos": json.dumps(productos)
#   })
#   → El SP crea factura + productos en UNA transaccion (todo o nada)
#
# Sin SPs: multiples llamadas SIN transaccion (riesgo de inconsistencia)
#   1. POST /api/factura            → crear cabecera
#   2. GET  /api/factura            → obtener el numero asignado
#   3. POST /api/productosporfactura (x N) → crear cada linea de detalle
#   Si falla en el paso 3, queda factura sin productos (inconsistente!)
# ══════════════════════════════════════════════════════════════════════

@bp.route('/factura/crear', methods=['POST'])
def crear():
    # ─── Extraer datos del formulario ────────────────────────────
    fkidcliente = request.form.get('fkidcliente', 0, type=int)
    fkidvendedor = request.form.get('fkidvendedor', 0, type=int)

    # Los productos vienen como arrays del formulario HTML:
    #   prod_codigo[]  = ["PR001", "PR002"]
    #   prod_cantidad[] = ["5", "3"]
    codigos = request.form.getlist('prod_codigo[]')
    cantidades = request.form.getlist('prod_cantidad[]')

    productos_lista = []
    for codigo, cantidad in zip(codigos, cantidades):
        if codigo and cantidad:
            productos_lista.append({"codigo": codigo, "cantidad": int(cantidad)})

    if not productos_lista:
        flash("Debe agregar al menos un producto.", "danger")
        return redirect(url_for('factura.nueva'))

    # ─── Calcular total en Python (con SPs lo hace la BD) ───────
    productos_catalogo = api.listar('producto')
    mapa_precios = {p.get('codigo'): float(p.get('valorunitario', 0)) for p in productos_catalogo}
    total = sum(p['cantidad'] * mapa_precios.get(p['codigo'], 0) for p in productos_lista)

    # ─── Paso 1: Crear la cabecera de la factura ────────────────
    datos_factura = {
        'fkidcliente': fkidcliente,
        'fkidvendedor': fkidvendedor,
        'total': total
    }
    exito, mensaje = api.crear('factura', datos_factura)

    if not exito:
        flash(f"Error al crear factura: {mensaje}", "danger")
        return redirect(url_for('factura.nueva'))

    # ─── Paso 2: Obtener el numero de la factura recien creada ──
    # Con SPs, el SP retorna el numero directamente.
    # Sin SPs, debemos buscar la ultima factura creada.
    facturas = api.listar('factura')
    if facturas:
        nueva_factura = max(facturas, key=lambda f: f.get('numero', 0))
        numero = nueva_factura.get('numero')

        # ─── Paso 3: Crear cada linea de detalle ────────────────
        # RIESGO: Si falla aqui, la factura queda sin productos.
        # Con SPs, esto estaria dentro de una transaccion.
        for prod in productos_lista:
            api.crear('productosporfactura', {
                'fknumerofactura': numero,
                'fkcodigoproducto': prod['codigo'],
                'cantidad': prod['cantidad']
            })

    flash("Factura creada exitosamente.", "success")
    return redirect(url_for('factura.index'))


# ══════════════════════════════════════════════════════════════════════
# FORMULARIO EDITAR FACTURA: GET /factura/editar/<numero>
# ══════════════════════════════════════════════════════════════════════

@bp.route('/factura/editar/<int:numero>')
def editar(numero):
    # Obtener la factura a editar
    facturas = api.listar('factura')
    factura = next((f for f in facturas if f.get('numero') == numero), None)

    if not factura:
        flash("Factura no encontrada.", "danger")
        return redirect(url_for('factura.index'))

    # Enriquecer con productos actuales
    _enriquecer_facturas([factura])

    # Cargar datos para los selects
    clientes = api.listar('cliente')
    vendedores = api.listar('vendedor')
    personas = api.listar('persona')
    productos = api.listar('producto')

    mapa_personas = {p.get('codigo'): p.get('nombre', '') for p in personas}
    for cli in clientes:
        cli['nombre'] = mapa_personas.get(cli.get('fkcodpersona'), 'Sin nombre')
    for ven in vendedores:
        ven['nombre'] = mapa_personas.get(ven.get('fkcodpersona'), 'Sin nombre')

    return render_template('pages/factura.html',
        vista='formulario', editando=True, factura=factura,
        clientes=clientes, vendedores=vendedores,
        productos_disponibles=productos
    )


# ══════════════════════════════════════════════════════════════════════
# ACTUALIZAR FACTURA: POST /factura/actualizar
# ══════════════════════════════════════════════════════════════════════
# Con SPs seria UNA llamada con transaccion:
#   api.ejecutar_sp("sp_actualizar_factura_y_productosporfactura", {...})
#   → El SP borra productos viejos + inserta nuevos + actualiza cabecera
#     todo dentro de BEGIN/COMMIT.
#
# Sin SPs: multiples llamadas SIN transaccion
#   1. PUT    /api/factura/numero/{N}              → actualizar cabecera
#   2. DELETE /api/productosporfactura/fknumerofactura/{N} → borrar viejos
#   3. POST   /api/productosporfactura (x N)       → insertar nuevos
# ══════════════════════════════════════════════════════════════════════

@bp.route('/factura/actualizar', methods=['POST'])
def actualizar():
    numero = request.form.get('numero', 0, type=int)
    fkidcliente = request.form.get('fkidcliente', 0, type=int)
    fkidvendedor = request.form.get('fkidvendedor', 0, type=int)

    codigos = request.form.getlist('prod_codigo[]')
    cantidades = request.form.getlist('prod_cantidad[]')

    productos_lista = []
    for codigo, cantidad in zip(codigos, cantidades):
        if codigo and cantidad:
            productos_lista.append({"codigo": codigo, "cantidad": int(cantidad)})

    if not productos_lista:
        flash("Debe agregar al menos un producto.", "danger")
        return redirect(url_for('factura.editar', numero=numero))

    # ─── Calcular total ─────────────────────────────────────────
    productos_catalogo = api.listar('producto')
    mapa_precios = {p.get('codigo'): float(p.get('valorunitario', 0)) for p in productos_catalogo}
    total = sum(p['cantidad'] * mapa_precios.get(p['codigo'], 0) for p in productos_lista)

    # ─── Paso 1: Actualizar cabecera ────────────────────────────
    datos_factura = {
        'fkidcliente': fkidcliente,
        'fkidvendedor': fkidvendedor,
        'total': total
    }
    exito, mensaje = api.actualizar('factura', 'numero', str(numero), datos_factura)

    if not exito:
        flash(f"Error al actualizar factura: {mensaje}", "danger")
        return redirect(url_for('factura.editar', numero=numero))

    # ─── Paso 2: Eliminar productos anteriores ──────────────────
    # DELETE /api/productosporfactura/fknumerofactura/{numero}
    # Esto elimina TODOS los productos asociados a esta factura.
    # RIESGO: Si el paso 3 falla, la factura queda sin productos.
    api.eliminar('productosporfactura', 'fknumerofactura', str(numero))

    # ─── Paso 3: Crear los nuevos productos ─────────────────────
    for prod in productos_lista:
        api.crear('productosporfactura', {
            'fknumerofactura': numero,
            'fkcodigoproducto': prod['codigo'],
            'cantidad': prod['cantidad']
        })

    flash("Factura actualizada exitosamente.", "success")
    return redirect(url_for('factura.index'))


# ══════════════════════════════════════════════════════════════════════
# ELIMINAR FACTURA: POST /factura/eliminar
# ══════════════════════════════════════════════════════════════════════
# Con SPs:
#   api.ejecutar_sp("sp_borrar_factura_y_productosporfactura",
#                    {"p_numero": numero})
#   → El SP borra productos + factura en transaccion.
#
# Sin SPs: 2 DELETEs separados (sin transaccion)
#   1. DELETE /api/productosporfactura/fknumerofactura/{N} → borrar detalle
#   2. DELETE /api/factura/numero/{N}                      → borrar cabecera
#   ORDEN IMPORTANTE: primero detalle, luego cabecera.
#   Si se borra la cabecera primero, los productos quedan huerfanos.
# ══════════════════════════════════════════════════════════════════════

@bp.route('/factura/eliminar', methods=['POST'])
def eliminar():
    numero = request.form.get('numero', 0, type=int)

    # Paso 1: Eliminar productos de la factura (detalle primero)
    api.eliminar('productosporfactura', 'fknumerofactura', str(numero))

    # Paso 2: Eliminar la factura (cabecera despues)
    exito, mensaje = api.eliminar('factura', 'numero', str(numero))

    if exito:
        flash("Factura eliminada exitosamente.", "success")
    else:
        flash(f"Error al eliminar factura: {mensaje}", "danger")

    return redirect(url_for('factura.index'))
