from fastapi import APIRouter, HTTPException, Query, Response, status
from services.fabrica_repositorios import crear_servicio_rol 

router = APIRouter(prefix="/rol", tags=["Roles"])

# --- OPERACIONES DE LECTURA ---

@router.get("/")
async def listar(esquema: str | None = Query(default=None), limite: int | None = Query(default=None)):
    """Retorna todos los roles. Esencial para llenar selects en el Front."""
    servicio = crear_servicio_rol()
    try:
        filas = await servicio.obtener_todos(esquema, limite)
        if not filas:
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        return {"tabla": "rol", "total": len(filas), "datos": filas}
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))
    finally:
        if hasattr(servicio, 'db'): await servicio.db.close()

@router.get("/{id}")
async def obtener_por_id(id: int, esquema: str | None = Query(default=None)):
    """Retorna un rol específico por su ID."""
    servicio = crear_servicio_rol()
    try:
        registro = await servicio.obtener_por_id(id, esquema)
        if not registro:
            raise HTTPException(status_code=404, detail="Rol no encontrado")
        return registro
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))
    finally:
        if hasattr(servicio, 'db'): await servicio.db.close()

# --- OPERACIONES DE ESCRITURA ---

@router.post("/", status_code=status.HTTP_201_CREATED)
async def crear(data: dict, esquema: str | None = Query(default=None)):
    servicio = crear_servicio_rol()
    try:
        if "id" in data: data.pop("id")
        exito, mensaje = await servicio.guardar(data, esquema)
        if exito:
            return {"mensaje": mensaje, "datos": data}
        raise HTTPException(status_code=400, detail=mensaje)
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))
    finally:
        if hasattr(servicio, 'db'): await servicio.db.close()

@router.put("/{id}")
async def actualizar(id: int, data: dict, esquema: str | None = Query(default=None)):
    servicio = crear_servicio_rol()
    try:
        exito, mensaje = await servicio.actualizar(id, data, esquema)
        if exito:
            return {"mensaje": mensaje}
        raise HTTPException(status_code=400, detail=mensaje)
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))
    finally:
        if hasattr(servicio, 'db'): await servicio.db.close()

@router.delete("/{id}")
async def eliminar(id: int, esquema: str | None = Query(default=None)):
    servicio = crear_servicio_rol()
    try:
        exito, mensaje = await servicio.eliminar(id, esquema)
        if exito:
            return {"mensaje": mensaje}
        raise HTTPException(status_code=400, detail=mensaje)
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))
    finally:
        if hasattr(servicio, 'db'): await servicio.db.close()