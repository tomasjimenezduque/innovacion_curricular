from fastapi import APIRouter, HTTPException, Query, Response, status
from services.fabrica_repositorios import crear_servicio_universidad

router = APIRouter(prefix="/universidad", tags=["Universidad"])

@router.get("/")
async def listar(esquema: str | None = Query(default=None), limite: int | None = Query(default=None)):
    servicio = crear_servicio_universidad()
    try:
        filas = await servicio.obtener_todos(esquema, limite)
        if not filas:
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        return {"tabla": "universidad", "total": len(filas), "datos": filas}
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))
    finally:
        if hasattr(servicio, 'db'): await servicio.db.close()

@router.get("/{id_u}")
async def obtener_por_id(id_u: int):
    servicio = crear_servicio_universidad()
    try:
        # Intento 1: Usar el método específico si existe
        if hasattr(servicio, 'obtener_por_id'):
            fila = await servicio.obtener_por_id(id_u)
        else:
            # Intento 2: Plan B (Filtrar de la lista completa si el repo no tiene el método)
            todas = await servicio.obtener_todos()
            fila = next((u for u in todas if u.get('id') == id_u), None)
        
        if not fila:
            raise HTTPException(status_code=404, detail="Universidad no encontrada")
        return fila
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Error en Backend: {str(ex)}")
    finally:
        if hasattr(servicio, 'db'): await servicio.db.close()

@router.post("/", status_code=status.HTTP_201_CREATED)
async def crear(data: dict, esquema: str | None = Query(default=None)):
    servicio = crear_servicio_universidad()
    try:
        if "id" in data and data["id"] is not None:
            data["id"] = int(data["id"])
        exito, mensaje = await servicio.guardar(data, esquema)
        if exito: return {"mensaje": mensaje, "datos": data}
        raise HTTPException(status_code=400, detail=mensaje)
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))
    finally:
        if hasattr(servicio, 'db'): await servicio.db.close()

@router.put("/{id_u}")
async def actualizar_uni(id_u: str, datos: dict):
    servicio = crear_servicio_universidad()
    try:
        id_int = int(id_u)
        if "id" in datos: datos.pop("id")
        exito, mensaje = await servicio.actualizar(id_int, datos)
        if exito: return {"mensaje": mensaje}
        raise HTTPException(status_code=400, detail=mensaje)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if hasattr(servicio, 'db'): await servicio.db.close()

@router.delete("/{id_u}")
async def eliminar_uni(id_u: str):
    servicio = crear_servicio_universidad()
    try:
        id_int = int(id_u)
        exito, mensaje = await servicio.eliminar(id_int)
        if exito: return {"mensaje": mensaje}
        raise HTTPException(status_code=400, detail=mensaje)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if hasattr(servicio, 'db'): await servicio.db.close()