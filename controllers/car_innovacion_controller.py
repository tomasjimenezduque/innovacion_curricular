
"""
car_innovacion_controller.py — Controller para la tabla car_innovacion
Generado automáticamente a partir del modelo.
"""

from fastapi import APIRouter, HTTPException, Query, Response
from models.car_innovacion import CarInnovacion
from servicios.fabrica_repositorios import crear_servicio_car_innovacion

router = APIRouter(prefix="/api/car_innovacion", tags=["CarInnovacion"])


@router.get("/")
async def listar(
    esquema: str | None = Query(default=None),
    limite: int | None = Query(default=None)
):
    try:
        servicio = crear_servicio_car_innovacion()
        filas = await servicio.listar(esquema, limite)

        if len(filas) == 0:
            return Response(status_code=204)

        return {
            "tabla": "car_innovacion",
            "total": len(filas),
            "datos": filas
        }
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))


@router.post("/")
async def crear(
    data: CarInnovacion,
    esquema: str | None = Query(default=None)
):
    try:
        datos = data.model_dump()

        servicio = crear_servicio_car_innovacion()
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
    data: CarInnovacion,
    esquema: str | None = Query(default=None)
):
    try:
        datos = data.model_dump()

        servicio = crear_servicio_car_innovacion()
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
        servicio = crear_servicio_car_innovacion()
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
