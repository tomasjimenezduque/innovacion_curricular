from fastapi import APIRouter, HTTPException, Query, Response, status
from services.fabrica_repositorios import crear_servicio_aliado
from models.aliado import Aliado

router = APIRouter(prefix="/aliado", tags=["Aliado"])

@router.get("/")
async def listar(
    esquema: str | None = Query(default=None),
    limite: int | None = Query(default=None)
):
    try:
        servicio = crear_servicio_aliado()
        filas = await servicio.obtener_todos(esquema, limite)

        if not filas:
            return Response(status_code=status.HTTP_204_NO_CONTENT)

        return {
            "tabla": "aliado",
            "total": len(filas),
            "datos": filas
        }
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))

@router.post("/", status_code=status.HTTP_201_CREATED)
async def crear(data: dict, esquema: str | None = Query(default=None)):
    try:
        servicio = crear_servicio_aliado()
        
        # --- CORRECCIÓN CRUCIAL PARA EL NIT ---
        # Si el NIT viene en los datos, lo forzamos a ser STRING 
        # para que PostgreSQL no grite (expected str, got int)
        if "nit" in data:
            data["nit"] = str(data["nit"])
        
        # Convertimos el diccionario a objeto modelo con el NIT ya como String
        nuevo_aliado = Aliado(**data) 
        
        exito, mensaje = await servicio.guardar(nuevo_aliado, esquema)

        if exito:
            return {"mensaje": mensaje, "datos": data}
        
        raise HTTPException(status_code=400, detail=mensaje)
    except Exception as ex:
        print(f"❌ ERROR: {ex}")
        raise HTTPException(status_code=500, detail=str(ex))
    
@router.put("/{nit}") # Cambié 'id' por 'nit' para ser consistente con tu PK
async def actualizar(
    nit: str, # El NIT es String
    data: dict,
    esquema: str | None = Query(default=None)
):
    try:
        servicio = crear_servicio_aliado()
        
        # Aseguramos que si el nit viene en el body, también sea string
        if "nit" in data:
            data["nit"] = str(data["nit"])

        exito, mensaje = await servicio.actualizar(nit, data, esquema)

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

@router.delete("/{nit}") # Cambié 'id' por 'nit'
async def eliminar(
    nit: str,
    esquema: str | None = Query(default=None)
):
    try:
        servicio = crear_servicio_aliado()
        
        entidad = await servicio.obtener_por_id(nit, esquema)
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