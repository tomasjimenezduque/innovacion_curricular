from fastapi import APIRouter, HTTPException, Query, Response, status
from services.fabrica_repositorios import crear_servicio_facultad

router = APIRouter(prefix="/facultad", tags=["Facultad"])

@router.get("/")
async def listar(
    esquema: str | None = Query(default=None),
    limite: int | None = Query(default=None)
):
    try:
        servicio = crear_servicio_facultad()
        filas = await servicio.obtener_todos(esquema, limite)

        if not filas:
            # Es mejor devolver lista vacía que un 204 para que el Front no rompa al iterar
            return {"tabla": "facultad", "total": 0, "datos": []}

        return {
            "tabla": "facultad",
            "total": len(filas),
            "datos": filas
        }
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))

# --- EL ENDPOINT QUE FALTABA Y CAUSABA EL 405 ---
@router.get("/{id}")
async def obtener_por_id(
    id: int,
    esquema: str | None = Query(default=None)
):
    try:
        servicio = crear_servicio_facultad()
        entidad = await servicio.obtener_por_id(id, esquema)
        
        if not entidad:
            raise HTTPException(status_code=404, detail="Facultad no encontrada")
            
        return entidad
    except HTTPException:
        raise
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))
# -----------------------------------------------

@router.post("/", status_code=status.HTTP_201_CREATED)
async def crear(
    data: dict, 
    esquema: str | None = Query(default=None)
):
    try:
        servicio = crear_servicio_facultad()
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
        
        entidad = await servicio.obtener_por_id(id, esquema)
        if not entidad:
            raise HTTPException(status_code=404, detail="Registro no encontrado")

        exito, mensaje = await servicio.eliminar(entidad, esquema)

        if exito:
            return {"mensaje": mensaje}
            
        raise HTTPException(status_code=400, detail=mensaje)
    except HTTPException:
        raise
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))