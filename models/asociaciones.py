from sqlalchemy import Table, Column, Integer, ForeignKeyConstraint, PrimaryKeyConstraint
from .base import Base

t_rol_usuario = Table(
    'rol_usuario', Base.metadata,
    Column('usuario_id', Integer, primary_key=True),
    Column('rol_id', Integer, primary_key=True),
    ForeignKeyConstraint(['rol_id'], ['rol.id'], ondelete='CASCADE', name='rol_usuario_rol_id_fkey'),
    ForeignKeyConstraint(['usuario_id'], ['usuario.id'], ondelete='CASCADE', name='rol_usuario_usuario_id_fkey'),
    PrimaryKeyConstraint('usuario_id', 'rol_id', name='rol_usuario_pkey')
)

t_programa_ac = Table(
    'programa_ac', Base.metadata,
    Column('programa', Integer, primary_key=True),
    Column('area_conocimiento', Integer, primary_key=True),
    ForeignKeyConstraint(['area_conocimiento'], ['area_conocimiento.id'], name='programa_ac_area_conocimiento_fkey'),
    ForeignKeyConstraint(['programa'], ['programa.id'], name='programa_ac_programa_fkey'),
    PrimaryKeyConstraint('programa', 'area_conocimiento', name='programa_ac_pkey')
)

t_an_programa = Table(
    'an_programa', Base.metadata,
    Column('aspecto_normativo', Integer, primary_key=True),
    Column('programa', Integer, primary_key=True),
    ForeignKeyConstraint(['aspecto_normativo'], ['aspecto_normativo.id'], name='an_programa_aspecto_normativo_fkey'),
    ForeignKeyConstraint(['programa'], ['programa.id'], name='an_programa_programa_fkey'),
    PrimaryKeyConstraint('aspecto_normativo', 'programa', name='an_programa_pkey')
)

t_programa_ci = Table(
    'programa_ci', Base.metadata,
    Column('programa', Integer, primary_key=True),
    Column('car_innovacion', Integer, primary_key=True),
    ForeignKeyConstraint(['car_innovacion'], ['car_innovacion.id'], name='programa_ci_car_innovacion_fkey'),
    ForeignKeyConstraint(['programa'], ['programa.id'], name='programa_ci_programa_fkey'),
    PrimaryKeyConstraint('programa', 'car_innovacion', name='programa_ci_pkey')
)

t_programa_pe = Table(
    'programa_pe', Base.metadata,
    Column('programa', Integer, primary_key=True),
    Column('practica_estrategia', Integer, primary_key=True),
    ForeignKeyConstraint(['practica_estrategia'], ['practica_estrategia.id'], name='programa_pe_practica_estrategia_fkey'),
    ForeignKeyConstraint(['programa'], ['programa.id'], name='programa_pe_programa_fkey'),
    PrimaryKeyConstraint('programa', 'practica_estrategia', name='programa_pe_pkey')
)

t_enfoque_rc = Table(
    'enfoque_rc', Base.metadata,
    Column('enfoque', Integer, primary_key=True),
    Column('registro_calificado', Integer, primary_key=True),
    ForeignKeyConstraint(['enfoque'], ['enfoque.id'], name='enfoque_rc_enfoque_fkey'),
    ForeignKeyConstraint(['registro_calificado'], ['registro_calificado.codigo'], name='enfoque_rc_registro_calificado_fkey'),
    PrimaryKeyConstraint('enfoque', 'registro_calificado', name='enfoque_rc_pkey')
)