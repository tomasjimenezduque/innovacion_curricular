
"""
aa_rc_controller.py — Controller para la tabla aa_rc
Generado automáticamente a partir del modelo.
"""

from fastapi import APIRouter, HTTPException, Query, Response
from models.aa_rc import AaRc
from servicios.fabrica_repositorios import crear_servicio_aa_rc

router = APIRouter(prefix="/api/aa_rc", tags=["AaRc"])


@router.get("/")
async def listar(
    esquema: str | None = Query(default=None),
    limite: int | None = Query(default=None)
):
    try:
        servicio = crear_servicio_aa_rc()
        filas = await servicio.listar(esquema, limite)

        if len(filas) == 0:
            return Response(status_code=204)

        return {
            "tabla": "aa_rc",
            "total": len(filas),
            "datos": filas
        }
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))


@router.post("/")
async def crear(
    data: AaRc,
    esquema: str | None = Query(default=None)
):
    try:
        datos = data.model_dump()

        servicio = crear_servicio_aa_rc()
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
    data: AaRc,
    esquema: str | None = Query(default=None)
):
    try:
        datos = data.model_dump()

        servicio = crear_servicio_aa_rc()
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
        servicio = crear_servicio_aa_rc()
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
