from fastapi import APIRouter, HTTPException, Query, Response, status
from services.fabrica_repositorios import crear_servicio_docente_departamento

router = APIRouter(prefix="/docente_departamento", tags=["DocenteDepartamento"])

@router.get("/")
async def listar(esquema: str | None = Query(default=None), limite: int | None = Query(default=None)):
    try:
        servicio = crear_servicio_docente_departamento()
        filas = await servicio.obtener_todos(esquema, limite)
        if not filas:
            return {"tabla": "docente_departamento", "total": 0, "datos": []}
        return {"tabla": "docente_departamento", "total": len(filas), "datos": filas}
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))

@router.get("/{docente}/{departamento}")
async def obtener_por_id(docente: int, departamento: int):
    try:
        servicio = crear_servicio_docente_departamento()
        fila = await servicio.obtener_por_id(docente, departamento)
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
        servicio = crear_servicio_docente_departamento()
        exito, mensaje = await servicio.guardar(data, esquema)
        if exito:
            return {"mensaje": mensaje, "datos": data}
        raise HTTPException(status_code=400, detail=mensaje)
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))

@router.put("/{docente}/{departamento}")
async def actualizar(docente: int, departamento: int, data: dict):
    try:
        servicio = crear_servicio_docente_departamento()
        data.pop('docente', None)
        data.pop('departamento', None)
        exito, mensaje = await servicio.actualizar(docente, departamento, data)
        if exito:
            return {"mensaje": mensaje}
        raise HTTPException(status_code=404, detail=mensaje)
    except HTTPException:
        raise
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))

@router.delete("/{docente}/{departamento}")
async def eliminar(docente: int, departamento: int):
    try:
        servicio = crear_servicio_docente_departamento()
        exito, mensaje = await servicio.eliminar(docente, departamento)
        if exito:
            return {"mensaje": mensaje}
        raise HTTPException(status_code=400, detail=mensaje)
    except HTTPException:
        raise
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))