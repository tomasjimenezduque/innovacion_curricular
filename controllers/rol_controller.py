from fastapi import APIRouter, HTTPException, Query, Response, status
from services.fabrica_repositorios import crear_servicio_facultad

router = APIRouter(prefix="/facultad", tags=["Facultad"])

@router.get("/")
async def listar(esquema: str | None = Query(default=None), limite: int | None = Query(default=None)):
    servicio = crear_servicio_facultad()
    try:
        filas = await servicio.obtener_todos(esquema, limite)
        if not filas:
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        return {"tabla": "facultad", "total": len(filas), "datos": filas}
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))
    finally:
        if hasattr(servicio, 'db'): await servicio.db.close()

@router.post("/", status_code=status.HTTP_201_CREATED)
async def crear(data: dict, esquema: str | None = Query(default=None)):
    servicio = crear_servicio_facultad()
    try:
        if "id" in data: data.pop("id")
        # El repo de Facultad debe manejar la conversión de fecha_fun si viene string
        exito, mensaje = await servicio.guardar(data, esquema)
        if exito:
            return {"mensaje": mensaje, "datos": data}
        raise HTTPException(status_code=400, detail=mensaje)
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))
    finally:
        if hasattr(servicio, 'db'): await servicio.db.close()

@router.delete("/{id}")
async def eliminar(id: int, esquema: str | None = Query(default=None)):
    servicio = crear_servicio_facultad()
    try:
        # Pasamos ID directo como en Rol
        exito, mensaje = await servicio.eliminar(id, esquema)
        if exito:
            return {"mensaje": mensaje}
        raise HTTPException(status_code=400, detail=mensaje)
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))
    finally:
        if hasattr(servicio, 'db'): await servicio.db.close()