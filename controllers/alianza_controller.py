from fastapi import APIRouter, HTTPException, Query, Response, status
from services.fabrica_repositorios import crear_servicio_alianza

router = APIRouter(prefix="/alianza", tags=["Alianza"])

@router.get("/")
async def listar(esquema: str | None = Query(default=None), limite: int | None = Query(default=None)):
    try:
        servicio = crear_servicio_alianza()
        filas = await servicio.obtener_todos(esquema, limite)
        if not filas:
            return {"tabla": "alianza", "total": 0, "datos": []}
        return {"tabla": "alianza", "total": len(filas), "datos": filas}
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))

@router.get("/{aliado}/{departamento}")
async def obtener_por_id(aliado: str, departamento: int):
    try:
        servicio = crear_servicio_alianza()
        fila = await servicio.obtener_por_id(aliado, departamento)
        if not fila:
            raise HTTPException(status_code=404, detail="Alianza no encontrada")
        return fila
    except HTTPException:
        raise
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))

@router.post("/", status_code=status.HTTP_201_CREATED)
async def crear(data: dict, esquema: str | None = Query(default=None)):
    try:
        servicio = crear_servicio_alianza()
        exito, mensaje = await servicio.guardar(data, esquema)
        if exito:
            return {"mensaje": mensaje, "datos": data}
        raise HTTPException(status_code=400, detail=mensaje)
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))

@router.put("/{aliado}/{departamento}")
async def actualizar(aliado: str, departamento: int, data: dict):
    try:
        servicio = crear_servicio_alianza()
        data.pop('aliado', None)
        data.pop('departamento', None)
        exito, mensaje = await servicio.actualizar(aliado, departamento, data)
        if exito:
            return {"mensaje": mensaje}
        raise HTTPException(status_code=404, detail=mensaje)
    except HTTPException:
        raise
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))

@router.delete("/{aliado}/{departamento}")
async def eliminar(aliado: str, departamento: int):
    try:
        servicio = crear_servicio_alianza()
        exito, mensaje = await servicio.eliminar(aliado, departamento)
        if exito:
            return {"mensaje": mensaje}
        raise HTTPException(status_code=400, detail=mensaje)
    except HTTPException:
        raise
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))    