from typing import Optional, List
from sqlalchemy import String, Integer, ForeignKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from .asociaciones import t_programa_ac, t_an_programa, t_programa_ci, t_programa_pe

class Programa(Base):
    __tablename__ = 'programa'
    __table_args__ = (
        ForeignKeyConstraint(['facultad'], ['facultad.id'], name='programa_facultad_fkey'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(60), nullable=False)
    tipo: Mapped[str] = mapped_column(String(45), nullable=False)
    nivel: Mapped[str] = mapped_column(String(45), nullable=False)
    fecha_creacion: Mapped[str] = mapped_column(String(45), nullable=False)
    numero_cohortes: Mapped[str] = mapped_column(String(45), nullable=False)
    cant_graduados: Mapped[str] = mapped_column(String(45), nullable=False)
    fecha_actualizacion: Mapped[str] = mapped_column(String(45), nullable=False)
    ciudad: Mapped[str] = mapped_column(String(45), nullable=False)
    facultad: Mapped[int] = mapped_column(Integer, nullable=False)
    fecha_cierre: Mapped[Optional[str]] = mapped_column(String(45))

    # Relaciones Many-to-Many
    area_conocimiento: Mapped[List['AreaConocimiento']] = relationship('AreaConocimiento', secondary=t_programa_ac, back_populates='programa')
    aspecto_normativo: Mapped[List['AspectoNormativo']] = relationship('AspectoNormativo', secondary=t_an_programa, back_populates='programa')
    car_innovacion: Mapped[List['CarInnovacion']] = relationship('CarInnovacion', secondary=t_programa_ci, back_populates='programa')
    practica_estrategia: Mapped[List['PracticaEstrategia']] = relationship('PracticaEstrategia', secondary=t_programa_pe, back_populates='programa')
    
    # Relaciones One-to-Many / Many-to-One
    facultad_: Mapped['Facultad'] = relationship('Facultad', back_populates='programa')
    acreditacion: Mapped[List['Acreditacion']] = relationship('Acreditacion', back_populates='programa_')
    activ_academica: Mapped[List['ActivAcademica']] = relationship('ActivAcademica', back_populates='programa')
    alianza: Mapped[List['Alianza']] = relationship('Alianza', back_populates='programa')
    docente_departamento: Mapped[List['DocenteDepartamento']] = relationship('DocenteDepartamento', back_populates='programa')
    pasantia: Mapped[List['Pasantia']] = relationship('Pasantia', back_populates='programa_')
    premio: Mapped[List['Premio']] = relationship('Premio', back_populates='programa_')
    registro_calificado: Mapped[List['RegistroCalificado']] = relationship('RegistroCalificado', back_populates='programa_')