# services/fabrica_repositorios.py
from database.connection import SessionLocal # Importa tu generador de sesiones
from repositories.aa_rc_repository import AaRcRepository

def crear_servicio_aa_rc():
    """
    Fábrica que instancia el repositorio inyectándole la sesión de BD.
    Esto permite que el controlador no tenga que saber NADA de SQLAlchemy.
    """
    # 1. Creamos una sesión de base de datos
    db = SessionLocal()
    
    try:
        # 2. Creamos el repositorio y le "inyectamos" la sesión
        repositorio = AaRcRepository(db)
        return repositorio
    finally:
        # Nota: En una API real, la sesión se suele cerrar 
        # después de la respuesta, pero para probar tu lógica inicial,
        # esto permitirá que el controlador reciba el objeto.
        pass

from repositories.acreditacion_repository import AcreditacionRepository

def crear_servicio_acreditacion():
    # Retornamos la instancia del repositorio con la sesión activa
    return AcreditacionRepository(SessionLocal())

from repositories.activ_academica_repository import ActivAcademicaRepository

def crear_servicio_activ_academica():
    # Instanciamos el repositorio con la sesión de la DB local
    return ActivAcademicaRepository(SessionLocal())

from repositories.aliado_repository import AliadoRepository

def crear_servicio_aliado():
    # Inyectamos la sesión local al repositorio de Aliados
    return AliadoRepository(SessionLocal())

from repositories.alianza_repository import AlianzaRepository

def crear_servicio_alianza():
    # Retornamos el repositorio de Alianza con la sesión inyectada
    return AlianzaRepository(SessionLocal())


from repositories.area_conocimiento_repository import AreaConocimientoRepository

def crear_servicio_area_conocimiento():
    # Retornamos el repositorio inyectando la sesión de base de datos
    return AreaConocimientoRepository(SessionLocal())


from repositories.aspecto_normativo_repository import AspectoNormativoRepository

def crear_servicio_aspecto_normativo():
    # Inyectamos la sesión y retornamos el repositorio de Aspecto Normativo
    return AspectoNormativoRepository(SessionLocal())

from repositories.car_innovacion_repository import CarInnovacionRepository

def crear_servicio_car_innovacion():
    # Retornamos el repositorio inyectando la sesión de base de datos local
    return CarInnovacionRepository(SessionLocal())

from repositories.docente_departamento_repository import DocenteDepartamentoRepository

def crear_servicio_docente_departamento():
    # Retornamos el repositorio estándar para la tabla DocenteDepartamento
    return DocenteDepartamentoRepository(SessionLocal())

from repositories.enfoque_repository import EnfoqueRepository

def crear_servicio_enfoque():
    # Retornamos la instancia del repositorio de Enfoque
    return EnfoqueRepository(SessionLocal())

from repositories.facultad_repository import FacultadRepository

def crear_servicio_facultad():
    # Retornamos el repositorio de Facultad inyectando la sesión de BD
    return FacultadRepository(SessionLocal())


from repositories.pasantia_repository import PasantiaRepository

def crear_servicio_pasantia():
    # Retornamos el repositorio inyectando la sesión de base de datos
    return PasantiaRepository(SessionLocal())


from repositories.practica_estrategia_repository import PracticaEstrategiaRepository

def crear_servicio_practica_estrategia():
    # Retornamos el repositorio inyectando la sesión de base de datos
    return PracticaEstrategiaRepository(SessionLocal())


from repositories.premio_repository import PremioRepository

def crear_servicio_premio():
    # Retornamos el repositorio inyectando la sesión de base de datos
    return PremioRepository(SessionLocal())



from repositories.programa_repository import ProgramaRepository

def crear_servicio_programa():
    # Retornamos el repositorio central del sistema
    return ProgramaRepository(SessionLocal())



from repositories.registro_calificado_repository import RegistroCalificadoRepository

def crear_servicio_registro_calificado():
    # Retornamos el repositorio inyectando la sesión actual
    return RegistroCalificadoRepository(SessionLocal())


from repositories.rol_repository import RolRepository

def crear_servicio_rol():
    # Inyectamos la sesión para la gestión de roles y permisos
    return RolRepository(SessionLocal())


from repositories.universidad_repository import UniversidadRepository

def crear_servicio_universidad():
    # Inyectamos la sesión para gestionar la entidad raíz del sistema
    return UniversidadRepository(SessionLocal())



from repositories.usuario_repository import UsuarioRepository

def crear_servicio_usuario():
    # Retornamos el repositorio inyectando la sesión de base de datos
    return UsuarioRepository(SessionLocal())