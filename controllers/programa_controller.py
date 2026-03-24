from fastapi import APIRouter, HTTPException, Query, Response, status
from services.fabrica_repositorios import crear_servicio_programa

router = APIRouter(prefix="/api/programa", tags=["Programa"])

@router.get("/")
async def listar(
    esquema: str | None = Query(default=None),
    limite: int | None = Query(default=None)
):
    try:
        servicio = crear_servicio_programa()
        # Ajuste: Sincronización con el método 'obtener_todos' del repo
        filas = await servicio.obtener_todos(esquema, limite)

        if not filas:
            return Response(status_code=status.HTTP_204_NO_CONTENT)

        return {
            "tabla": "programa",
            "total": len(filas),
            "datos": filas
        }
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))

@router.post("/", status_code=status.HTTP_201_CREATED)
async def crear(
    data: dict, # Recibimos dict para evitar conflictos con el modelo de base de datos
    esquema: str | None = Query(default=None)
):
    try:
        servicio = crear_servicio_programa()
        # Ajuste: Interpretamos la tupla (exito, mensaje) del repositorio
        exito, mensaje = await servicio.guardar(data, esquema)

        if exito:
            return {
                "mensaje": mensaje,
                "datos": data
            }
        
        raise HTTPException(status_code=400, detail=mensaje)
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))

@router.put("/{id}")
async def actualizar(
    id: int,
    data: dict,
    esquema: str | None = Query(default=None)
):
    try:
        servicio = crear_servicio_programa()
        # Ajuste: El repo ahora retorna éxito y mensaje en lugar de filas
        exito, mensaje = await servicio.actualizar(id, data, esquema)

        if exito:
            return {
                "mensaje": mensaje,
                "datos_actualizados": data
            }
        
        raise HTTPException(status_code=404, detail=mensaje)
    except HTTPException:
        raise
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))

@router.delete("/{id}")
async def eliminar(
    id: int,
    esquema: str | None = Query(default=None)
):
    try:
        servicio = crear_servicio_programa()
        
        # Primero buscamos la entidad para asegurar que el objeto esté cargado
        entidad = await servicio.obtener_por_id(id, esquema)
        if not entidad:
            raise HTTPException(status_code=404, detail="Registro no encontrado")

        exito, mensaje = await servicio.eliminar(entidad, esquema)

        if exito:
            return {"mensaje": mensaje}
            
        # Útil si el programa tiene restricciones de integridad (ej: proyectos asociados)
        raise HTTPException(status_code=400, detail=mensaje)
    except HTTPException:
        raise
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))