from fastapi import APIRouter, HTTPException, Query, Response, status
from services.fabrica_repositorios import crear_servicio_usuario

router = APIRouter(prefix="/usuario", tags=["Usuario"])

# --- OBTENER TODOS ---
@router.get("/")
async def listar(esquema: str | None = Query(default=None), limite: int | None = Query(default=None)):
    servicio = crear_servicio_usuario()
    try:
        filas = await servicio.obtener_todos(esquema, limite)
        return {
            "tabla": "usuario",
            "total": len(filas) if filas else 0,
            "datos": filas or []
        }
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))
    finally:
        await servicio.db.close()

# --- OBTENER UNO (El que faltaba para el Edit) ---
@router.get("/{id}")
async def obtener_por_id(id: int, esquema: str | None = Query(default=None)):
    servicio = crear_servicio_usuario()
    try:
        entidad = await servicio.obtener_por_id(id, esquema)
        if not entidad:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return entidad
    except HTTPException:
        raise
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))
    finally:
        await servicio.db.close()

# --- CREAR (Sin {id} en la ruta) ---
@router.post("/", status_code=status.HTTP_201_CREATED)
async def crear(data: dict, esquema: str | None = Query(default=None)):
    servicio = crear_servicio_usuario()
    try:
        # 1. Limpieza de campos que no van en la tabla 'usuario'
        id_rol = data.pop('id_rol', None) 
        
        # 2. Validación preventiva (evita el 500 si falta data básica)
        if not data.get('username') or not data.get('password'):
            raise HTTPException(status_code=400, detail="Username y Password son requeridos")

        print(f"DEBUG: Creando usuario con datos limpios: {data}")
        
        exito, mensaje = await servicio.guardar(data, esquema)
        
        if exito:
            # Aquí podrías usar id_rol para insertar en la tabla intermedia
            # si tu servicio tiene un método como: 
            # await servicio.asignar_rol(nuevo_id, id_rol)
            return {"mensaje": mensaje, "datos": data}
        
        raise HTTPException(status_code=400, detail=mensaje)
    except Exception as ex:
        print(f"ERROR EN POST: {str(ex)}")
        raise HTTPException(status_code=500, detail=f"Error interno: {str(ex)}")
    finally:
        await servicio.db.close()

# --- ACTUALIZAR ---
@router.put("/{id}")
async def actualizar(id: int, data: dict, esquema: str | None = Query(default=None)):
    servicio = crear_servicio_usuario()
    try:
        # 1. Extraemos los campos que NO pertenecen a la tabla 'usuario'
        # para procesarlos por separado o simplemente descartarlos.
        id_rol = data.pop('id_rol', None) 
        
        # 2. También es buena práctica quitar el 'id' si viene en el body
        data.pop('id', None)

        print(f"DEBUG: Datos limpios para SQLAlchemy: {data}")
        
        exito, mensaje = await servicio.actualizar(id, data, esquema)
        
        # 3. (Opcional) Si quieres actualizar el rol, aquí llamarías 
        # a un método del servicio: await servicio.asignar_rol(id, id_rol)

        if exito:
            return {"mensaje": mensaje, "datos_actualizados": data}
        
        raise HTTPException(status_code=404, detail=mensaje)
    except Exception as ex:
        print(f"ERROR CRÍTICO EN PUT: {str(ex)}") 
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(ex)}")
    finally:
        await servicio.db.close()

# --- ELIMINAR ---
@router.delete("/{id}")
async def eliminar(id: int, esquema: str | None = Query(default=None)):
    servicio = crear_servicio_usuario()
    try:
        entidad = await servicio.obtener_por_id(id, esquema)
        if not entidad:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        exito, mensaje = await servicio.eliminar(entidad, esquema)
        if exito:
            return {"mensaje": mensaje}
        raise HTTPException(status_code=400, detail=mensaje)
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))
    finally:
        await servicio.db.close()