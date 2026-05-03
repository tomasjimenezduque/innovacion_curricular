from fastapi import APIRouter, HTTPException, Query, Response, status
from services.fabrica_repositorios import crear_servicio_aliado
from models.aliado import Aliado

router = APIRouter(prefix="/aliado", tags=["Aliado"])

@router.get("/")
async def listar(esquema: str | None = Query(default=None), limite: int | None = Query(default=None)):
    servicio = crear_servicio_aliado()
    try:
        filas = await servicio.obtener_todos(esquema, limite)
        if not filas:
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        return {"tabla": "aliado", "total": len(filas), "datos": filas}
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))
    finally:
        # Esto es lo que evita que se saturen las conexiones en Postgres
        if hasattr(servicio, 'db'): await servicio.db.close()

@router.get("/{id}")
async def obtener_por_id(id: str):
    servicio = crear_servicio_aliado()
    try:
        # En Aliado, el ID suele ser el NIT (string)
        fila = await servicio.obtener_por_id(id)
        
        if not fila:
            raise HTTPException(status_code=404, detail="Aliado no encontrado")
        return fila
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Error en Backend: {str(ex)}")
    finally:
        if hasattr(servicio, 'db'): await servicio.db.close()

@router.post("/", status_code=status.HTTP_201_CREATED)
async def crear(data: dict, esquema: str | None = Query(default=None)):
    servicio = crear_servicio_aliado()
    try:
        # Aseguramos que el NIT sea string si viene en el body
        if "nit" in data:
            data["nit"] = str(data["nit"])
            
        nuevo_aliado = Aliado(**data)
        exito, mensaje = await servicio.guardar(nuevo_aliado, esquema)
        
        if exito: 
            return {"mensaje": mensaje, "datos": data}
        raise HTTPException(status_code=400, detail=mensaje)
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))
    finally:
        if hasattr(servicio, 'db'): await servicio.db.close()

@router.put("/{id}")
async def actualizar(id: str, datos: dict):
    servicio = crear_servicio_aliado()
    try:
        # Limpieza de datos: el ID de la URL manda sobre el del body
        if "id" in datos: datos.pop("id")
        if "nit" in datos: datos["nit"] = str(datos["nit"])
            
        exito, mensaje = await servicio.actualizar(id, datos)
        if exito: return {"mensaje": mensaje}
        raise HTTPException(status_code=400, detail=mensaje)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if hasattr(servicio, 'db'): await servicio.db.close()

@router.delete("/{id}")
async def eliminar(id: str):
    servicio = crear_servicio_aliado()
    try:
        # Primero buscamos la entidad para poder pasarla al método eliminar
        entidad = await servicio.obtener_por_id(id)
        if not entidad:
            raise HTTPException(status_code=404, detail="Aliado no encontrado")
            
        exito, mensaje = await servicio.eliminar(entidad)
        if exito: return {"mensaje": mensaje}
        raise HTTPException(status_code=400, detail=mensaje)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if hasattr(servicio, 'db'): await servicio.db.close()