from fastapi import APIRouter, HTTPException, Query, Response, status
from services.fabrica_repositorios import crear_servicio_asociaciones
from models.asociaciones import (
    t_rol_usuario, t_programa_ac, t_an_programa, 
    t_programa_ci, t_programa_pe, t_enfoque_rc
)

router = APIRouter(prefix="/asociaciones", tags=["Asociaciones"])

# Diccionario para mapear el nombre que viene del cliente con el objeto Table de SQLAlchemy
MAPA_TABLAS = {
    "rol_usuario": t_rol_usuario,
    "programa_area": t_programa_ac,
    "programa_normativo": t_an_programa,
    "programa_innovacion": t_programa_ci,
    "programa_estrategia": t_programa_pe,
    "enfoque_registro": t_enfoque_rc
}

@router.post("/", status_code=status.HTTP_201_CREATED)
async def crear_asociacion(
    nombre_tabla: str, # Ejemplo: "rol_usuario"
    data: dict
):
    """
    Crea una relación en una tabla intermedia.
    data debe contener las llaves necesarias (ej: {"usuario_id": 1, "rol_id": 2})
    """
    try:
        if nombre_tabla not in MAPA_TABLAS:
            raise HTTPException(status_code=400, detail="La tabla de asociación no es válida")

        servicio = crear_servicio_asociaciones()
        
        # Usamos el método de inserción que definimos en el repo
        # Nota: Si definiste métodos específicos (asociar_rol_usuario), úsalos.
        # Aquí usaré una lógica genérica basada en tu nuevo repo:
        exito, mensaje = await servicio.asociar_generico(MAPA_TABLAS[nombre_tabla], data)

        if exito:
            return {"mensaje": mensaje, "datos": data}
        
        raise HTTPException(status_code=400, detail=mensaje)
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))

@router.delete("/")
async def eliminar_asociacion(
    nombre_tabla: str,
    id_1: int,
    id_2: int,
    nombre_col_1: str,
    nombre_col_2: str
):
    """
    Elimina una relación específica. 
    Ejemplo: /asociaciones/?nombre_tabla=rol_usuario&id_1=1&id_2=2&nombre_col_1=usuario_id&nombre_col_2=rol_id
    """
    try:
        if nombre_tabla not in MAPA_TABLAS:
            raise HTTPException(status_code=400, detail="Tabla no válida")

        servicio = crear_servicio_asociaciones()
        filtros = {nombre_col_1: id_1, nombre_col_2: id_2}
        
        exito, mensaje = await servicio.eliminar_asociacion(MAPA_TABLAS[nombre_tabla], filtros)

        if exito:
            return {"mensaje": mensaje}
            
        raise HTTPException(status_code=400, detail=mensaje)
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))