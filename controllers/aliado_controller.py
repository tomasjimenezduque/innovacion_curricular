from fastapi import APIRouter, HTTPException, Query, Response, status
from services.fabrica_repositorios import crear_servicio_aliado
from models.aliado import Aliado

router = APIRouter(prefix="/aliado", tags=["Aliado"])

@router.get("/")
async def listar(
    esquema: str | None = Query(default=None),
    limite: int | None = Query(default=None)
):
    try:
        servicio = crear_servicio_aliado()
        filas = await servicio.obtener_todos(esquema, limite)
        if not filas:
            return {"tabla": "aliado", "total": 0, "datos": []}
        return {"tabla": "aliado", "total": len(filas), "datos": filas}
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))

@router.get("/{nit}")
async def obtener_por_id(nit: str):
    try:
        servicio = crear_servicio_aliado()
        fila = await servicio.obtener_por_id(nit)
        if not fila:
            raise HTTPException(status_code=404, detail="Aliado no encontrado")
        return fila
    except HTTPException:
        raise
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))

@router.post("/", status_code=status.HTTP_201_CREATED)
async def crear(data: dict, esquema: str | None = Query(default=None)):
    try:
        servicio = crear_servicio_aliado()
        if "nit" in data:
            data["nit"] = str(data["nit"])
        nuevo_aliado = Aliado(**data)
        exito, mensaje = await servicio.guardar(nuevo_aliado, esquema)
        if exito:
            return {"mensaje": mensaje, "datos": data}
        raise HTTPException(status_code=400, detail=mensaje)
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))

@router.put("/{nit}")
async def actualizar(nit: str, data: dict, esquema: str | None = Query(default=None)):
    try:
        servicio = crear_servicio_aliado()
        data.pop('nit', None)
        exito, mensaje = await servicio.actualizar(nit, data, esquema)
        if exito:
            return {"mensaje": mensaje}
        raise HTTPException(status_code=404, detail=mensaje)
    except HTTPException:
        raise
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))

@router.delete("/{nit}")
async def eliminar(nit: str, esquema: str | None = Query(default=None)):
    try:
        servicio = crear_servicio_aliado()
        entidad = await servicio.obtener_por_id(nit, esquema)
        if not entidad:
            raise HTTPException(status_code=404, detail="Aliado no encontrado")
        exito, mensaje = await servicio.eliminar(entidad, esquema)
        if exito:
            return {"mensaje": mensaje}
        raise HTTPException(status_code=400, detail=mensaje)
    except HTTPException:
        raise
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))