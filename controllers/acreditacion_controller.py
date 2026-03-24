from fastapi import APIRouter, HTTPException, Query, Response, status
from servicios.fabrica_repositorios import crear_servicio_acreditacion

# Nota: Para 'data: dict', en el futuro usaremos Pydantic Schemas
router = APIRouter(prefix="/api/acreditacion", tags=["Acreditacion"])

@router.get("/")
async def listar(
    esquema: str | None = Query(default=None),
    limite: int | None = Query(default=None)
):
    try:
        servicio = crear_servicio_acreditacion()
        # Ajuste: método 'obtener_todos'
        filas = await servicio.obtener_todos(esquema, limite)

        if not filas:
            return Response(status_code=status.HTTP_204_NO_CONTENT)

        return {
            "tabla": "acreditacion",
            "total": len(filas),
            "datos": filas
        }
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))

@router.post("/", status_code=status.HTTP_201_CREATED)
async def crear(
    data: dict, # Cambiado a dict para evitar conflicto con el modelo de SQLAlchemy
    esquema: str | None = Query(default=None)
):
    try:
        servicio = crear_servicio_acreditacion()
        # Ajuste: método 'guardar' devuelve (bool, mensaje)
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
        servicio = crear_servicio_acreditacion()
        # Ajuste: método 'actualizar' devuelve (bool, mensaje)
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
        servicio = crear_servicio_acreditacion()
        
        # Primero buscamos la entidad (necesaria para el método eliminar del repo)
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