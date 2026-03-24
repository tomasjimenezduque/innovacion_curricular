from fastapi import APIRouter, HTTPException, Query, Response, status
from services.fabrica_repositorios import crear_servicio_facultad

router = APIRouter(prefix="/api/facultad", tags=["Facultad"])

@router.get("/")
async def listar(
    esquema: str | None = Query(default=None),
    limite: int | None = Query(default=None)
):
    try:
        servicio = crear_servicio_facultad()
        # Ajuste: Sincronización con el método del repositorio
        filas = await servicio.obtener_todos(esquema, limite)

        if not filas:
            return Response(status_code=status.HTTP_204_NO_CONTENT)

        return {
            "tabla": "facultad",
            "total": len(filas),
            "datos": filas
        }
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))

@router.post("/", status_code=status.HTTP_201_CREATED)
async def crear(
    data: dict, # Evitamos conflictos de validación con el modelo SQLAlchemy
    esquema: str | None = Query(default=None)
):
    try:
        servicio = crear_servicio_facultad()
        # Ajuste: Interpretamos la tupla (exito, mensaje)
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
        servicio = crear_servicio_facultad()
        # Ajuste: Cambio de lógica de 'filas' a booleano de éxito
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
        servicio = crear_servicio_facultad()
        
        # Primero buscamos la entidad para pasar el objeto al repositorio
        entidad = await servicio.obtener_por_id(id, esquema)
        if not entidad:
            raise HTTPException(status_code=404, detail="Registro no encontrado")

        exito, mensaje = await servicio.eliminar(entidad, esquema)

        if exito:
            return {"mensaje": mensaje}
            
        # Si hay dependencias, el mensaje del repo explicará por qué falló
        raise HTTPException(status_code=400, detail=mensaje)
    except HTTPException:
        raise
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))