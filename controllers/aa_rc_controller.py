from fastapi import APIRouter, HTTPException, Query, Response, status
from services.fabrica_repositorios import crear_servicio_aa_rc

router = APIRouter(prefix="/api/aa_rc", tags=["AaRc"])

@router.get("/", response_model=None)
async def listar(
    esquema: str | None = Query(default=None),
    limite: int | None = Query(default=None)
):
    try:
        servicio = crear_servicio_aa_rc()
        # Cambio: método coincidente con el repositorio
        filas = await servicio.obtener_todos(esquema, limite)

        if not filas:
            return Response(status_code=status.HTTP_204_NO_CONTENT)

        return {
            "tabla": "aa_rc",
            "total": len(filas),
            "datos": filas
        }
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=None)
async def crear(
    data: dict, 
    esquema: str | None = Query(default=None)
):
    try:
        servicio = crear_servicio_aa_rc()
        # Importante: Aquí 'data' debería convertirse en la entidad AaRc 
        # antes de enviarse al repo, o el repo debe manejar el dict.
        exito, mensaje = await servicio.guardar(data, esquema)

        if exito:
            return {
                "mensaje": mensaje,
                "datos": data
            }
        raise HTTPException(status_code=400, detail=mensaje)
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))

@router.put("/{id_curso}/{cod_reg}", response_model=None)
async def actualizar(
    id_curso: int,
    cod_reg: int,
    data: dict,
    esquema: str | None = Query(default=None)
):
    try:
        servicio = crear_servicio_aa_rc()
        # NOTA: En llaves compuestas, el método actualizar debe recibir ambos IDs
        # Asegúrate de que AaRcRepository.actualizar soporte esta firma.
        exito, mensaje = await servicio.actualizar(id_curso, cod_reg, data, esquema)

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

@router.delete("/{id_curso}/{cod_reg}", response_model=None)
async def eliminar(
    id_curso: int,
    cod_reg: int,
    esquema: str | None = Query(default=None)
):
    try:
        servicio = crear_servicio_aa_rc()
        # Primero obtenemos la entidad para poder pasarla al método eliminar del repo
        entidad = await servicio.obtener_por_id_compuesto(id_curso, cod_reg, esquema)
        
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