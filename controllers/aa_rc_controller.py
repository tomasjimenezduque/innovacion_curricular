from fastapi import APIRouter, HTTPException, Query, Response, status
from services.fabrica_repositorios import crear_servicio_aa_rc

router = APIRouter(prefix="/aa_rc", tags=["AaRc"])

@router.get("/")
async def listar(esquema: str | None = Query(default=None), limite: int | None = Query(default=None)):
    try:
        servicio = crear_servicio_aa_rc()
        filas = await servicio.obtener_todos(esquema, limite)
        if not filas:
            return {"tabla": "aa_rc", "total": 0, "datos": []}
        return {"tabla": "aa_rc", "total": len(filas), "datos": filas}
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))

@router.get("/{id_curso}/{cod_reg}")
async def obtener_por_id(id_curso: int, cod_reg: int):
    try:
        servicio = crear_servicio_aa_rc()
        fila = await servicio.obtener_por_llave_compuesta(id_curso, cod_reg)
        if not fila:
            raise HTTPException(status_code=404, detail="Registro no encontrado")
        return fila
    except HTTPException:
        raise
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))

@router.post("/", status_code=status.HTTP_201_CREATED)
async def crear(data: dict, esquema: str | None = Query(default=None)):
    try:
        servicio = crear_servicio_aa_rc()
        exito, mensaje = await servicio.guardar(data, esquema)
        if exito:
            return {"mensaje": mensaje, "datos": data}
        raise HTTPException(status_code=400, detail=mensaje)
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))

@router.put("/{id_curso}/{cod_reg}")
async def actualizar(id_curso: int, cod_reg: int, data: dict):
    try:
        servicio = crear_servicio_aa_rc()
        data.pop('activ_academicas_idcurso', None)
        data.pop('registro_calificado_codigo', None)
        exito, mensaje = await servicio.actualizar(id_curso, cod_reg, data)
        if exito:
            return {"mensaje": mensaje}
        raise HTTPException(status_code=404, detail=mensaje)
    except HTTPException:
        raise
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))

@router.delete("/{id_curso}/{cod_reg}")
async def eliminar(id_curso: int, cod_reg: int):
    try:
        servicio = crear_servicio_aa_rc()
        exito, mensaje = await servicio.eliminar(id_curso, cod_reg)
        if exito:
            return {"mensaje": mensaje}
        raise HTTPException(status_code=400, detail=mensaje)
    except HTTPException:
        raise
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))