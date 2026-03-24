from fastapi import APIRouter, HTTPException, Query, Response, status
from services.fabrica_repositorios import crear_servicio_enfoque

router = APIRouter(prefix="/api/enfoque", tags=["Enfoque"])

@router.get("/")
async def listar(
    esquema: str | None = Query(default=None),
    limite: int | None = Query(default=None)
):
    try:
        servicio = crear_servicio_enfoque()
        # Ajuste: Sincronización con 'obtener_todos'
        filas = await servicio.obtener_todos(esquema, limite)

        if not filas:
            return Response(status_code=status.HTTP_204_NO_CONTENT)

        return {
            "tabla": "enfoque",
            "total": len(filas),
            "datos": filas
        }
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))

@router.post("/", status_code=status.HTTP_201_CREATED)
async def crear(
    data: dict, # Recibimos dict para evitar conflictos con el modelo de SQLAlchemy
    esquema: str | None = Query(default=None)
):
    try:
        servicio = crear_servicio_enfoque()
        # Ajuste: El método 'guardar' devuelve (exito, mensaje)
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
        servicio = crear_servicio_enfoque()
        # Ajuste: 'actualizar' ahora procesa el retorno (bool, str)
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
        servicio = crear_servicio_enfoque()
        
        # Obtenemos la entidad primero para el método eliminar del repo
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
