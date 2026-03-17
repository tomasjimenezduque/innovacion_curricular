
"""
asociaciones_controller.py — Controller para la tabla asociaciones
Generado automáticamente a partir del modelo.
"""

from fastapi import APIRouter, HTTPException, Query, Response
from models.asociaciones import Asociaciones
from servicios.fabrica_repositorios import crear_servicio_asociaciones

router = APIRouter(prefix="/api/asociaciones", tags=["Asociaciones"])


@router.get("/")
async def listar(
    esquema: str | None = Query(default=None),
    limite: int | None = Query(default=None)
):
    try:
        servicio = crear_servicio_asociaciones()
        filas = await servicio.listar(esquema, limite)

        if len(filas) == 0:
            return Response(status_code=204)

        return {
            "tabla": "asociaciones",
            "total": len(filas),
            "datos": filas
        }
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))


@router.post("/")
async def crear(
    data: Asociaciones,
    esquema: str | None = Query(default=None)
):
    try:
        datos = data.model_dump()

        servicio = crear_servicio_asociaciones()
        creado = await servicio.crear(datos, esquema)

        if creado:
            return {
                "estado": 200,
                "mensaje": "Registro creado",
                "datos": datos
            }

    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))


@router.put("/{id}")
async def actualizar(
    id: int,
    data: Asociaciones,
    esquema: str | None = Query(default=None)
):
    try:
        datos = data.model_dump()

        servicio = crear_servicio_asociaciones()
        filas = await servicio.actualizar(id, datos, esquema)

        if filas > 0:
            return {
                "estado": 200,
                "mensaje": "Registro actualizado",
                "filasAfectadas": filas
            }
        else:
            raise HTTPException(status_code=404, detail="Registro no encontrado")

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
        servicio = crear_servicio_asociaciones()
        filas = await servicio.eliminar(id, esquema)

        if filas > 0:
            return {
                "estado": 200,
                "mensaje": "Registro eliminado",
                "filasEliminadas": filas
            }
        else:
            raise HTTPException(status_code=404, detail="Registro no encontrado")

    except HTTPException:
        raise
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))
