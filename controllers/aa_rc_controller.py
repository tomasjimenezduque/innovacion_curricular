from fastapi import APIRouter, HTTPException, Query, Response, status
from services.fabrica_repositorios import crear_servicio_aa_rc

# Eliminamos la importación de AaRc aquí para evitar que FastAPI intente validarlo como Pydantic
router = APIRouter(prefix="/api/aa_rc", tags=["AaRc"])

@router.get("/", response_model=None)
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

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=None)
async def crear(
    data: dict, # CAMBIO: Recibimos un dict genérico para evitar el error de Pydantic
    esquema: str | None = Query(default=None)
):
    try:
        servicio = crear_servicio_aa_rc()
        # Pasamos el dict directamente al servicio
        creado = await servicio.crear(data, esquema)

        if creado:
            return {
                "mensaje": "Registro creado con éxito",
                "datos": data
            }
        raise HTTPException(status_code=400, detail="No se pudo crear el registro")
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))

@router.put("/{id_curso}/{cod_reg}", response_model=None)
async def actualizar(
    id_curso: int,
    cod_reg: int,
    data: dict, # CAMBIO: Recibimos un dict genérico
    esquema: str | None = Query(default=None)
):
    try:
        servicio = crear_servicio_aa_rc()
        # El servicio recibe ambos IDs de la llave compuesta y el diccionario de datos
        filas = await servicio.actualizar(id_curso, cod_reg, data, esquema)

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

@router.delete("/{id_curso}/{cod_reg}", response_model=None)
async def eliminar(
    id_curso: int,
    cod_reg: int,
    esquema: str | None = Query(default=None)
):
    try:
        servicio = crear_servicio_aa_rc()
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