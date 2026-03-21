from fastapi import APIRouter, HTTPException, Query, Response, status
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

        if not filas:
            return Response(status_code=status.HTTP_204_NO_CONTENT)

        return {
            "tabla": "aa_rc",
            "total": len(filas),
            "datos": filas
        }
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))

@router.post("/", status_code=status.HTTP_201_CREATED)
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
                "mensaje": "Registro creado con éxito",
                "datos": datos
            }
        raise HTTPException(status_code=400, detail="No se pudo crear el registro")
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))

# CAMBIO CRÍTICO: PUT ahora recibe dos parámetros para la llave compuesta
@router.put("/{id_curso}/{cod_reg}")
async def actualizar(
    id_curso: int,
    cod_reg: int,
    data: AaRc,
    esquema: str | None = Query(default=None)
):
    try:
        datos = data.model_dump()
        servicio = crear_servicio_aa_rc()
        # El servicio debe recibir ambos identificadores
        filas = await servicio.actualizar(id_curso, cod_reg, datos, esquema)

        if filas > 0:
            return {
                "mensaje": "Registro actualizado",
                "filasAfectadas": filas
            }
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    except HTTPException:
        raise
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))

# CAMBIO CRÍTICO: DELETE ahora recibe dos parámetros
@router.delete("/{id_curso}/{cod_reg}")
async def eliminar(
    id_curso: int,
    cod_reg: int,
    esquema: str | None = Query(default=None)
):
    try:
        servicio = crear_servicio_aa_rc()
        # El servicio debe recibir ambos identificadores
        filas = await servicio.eliminar(id_curso, cod_reg, esquema)

        if filas > 0:
            return {
                "mensaje": "Registro eliminado",
                "filasEliminadas": filas
            }
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    except HTTPException:
        raise
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))
