from fastapi import APIRouter, HTTPException, Query, status
from services.fabrica_repositorios import crear_servicio_car_innovacion

router = APIRouter(prefix="/car_innovacion", tags=["CarInnovacion"])

@router.get("/")
async def listar(esquema: str | None = Query(default=None), limite: int | None = Query(default=None)):
    try:
        servicio = crear_servicio_car_innovacion()
        filas = await servicio.obtener_todos(esquema, limite)
        if not filas:
            return {"tabla": "car_innovacion", "total": 0, "datos": []}
        return {"tabla": "car_innovacion", "total": len(filas), "datos": filas}
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))

@router.get("/{id}")
async def obtener_por_id(id: int):
    try:
        servicio = crear_servicio_car_innovacion()
        fila = await servicio.obtener_por_id(id)
        if not fila:
            raise HTTPException(status_code=404, detail="Característica no encontrada")
        return fila
    except HTTPException:
        raise
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))

@router.post("/", status_code=status.HTTP_201_CREATED)
async def crear(data: dict, esquema: str | None = Query(default=None)):
    try:
        servicio = crear_servicio_car_innovacion()
        exito, mensaje = await servicio.guardar(data, esquema)
        if exito:
            return {"mensaje": mensaje, "datos": data}
        raise HTTPException(status_code=400, detail=mensaje)
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))

@router.put("/{id}")
async def actualizar(id: int, data: dict):
    try:
        servicio = crear_servicio_car_innovacion()
        data.pop('id', None)
        exito, mensaje = await servicio.actualizar(id, data)
        if exito:
            return {"mensaje": mensaje}
        raise HTTPException(status_code=404, detail=mensaje)
    except HTTPException:
        raise
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))

@router.delete("/{id}")
async def eliminar(id: int):
    try:
        servicio = crear_servicio_car_innovacion()
        entidad = await servicio.obtener_por_id(id)
        if not entidad:
            raise HTTPException(status_code=404, detail="Característica no encontrada")
        exito, mensaje = await servicio.eliminar(entidad)
        if exito:
            return {"mensaje": mensaje}
        raise HTTPException(status_code=400, detail=mensaje)
    except HTTPException:
        raise
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))