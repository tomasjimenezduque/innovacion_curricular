from typing import Optional, List
from sqlalchemy import String, Integer, SmallInteger, ForeignKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

class ActivAcademica(Base):
    __tablename__ = 'activ_academica'
    __table_args__ = (
        ForeignKeyConstraint(['disenio'], ['programa.id'], name='activ_academica_disenio_fkey'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(45), nullable=False)
    num_creditos: Mapped[int] = mapped_column(Integer, nullable=False)
    tipo: Mapped[str] = mapped_column(String(20), nullable=False)
    area_formacion: Mapped[str] = mapped_column(String(45), nullable=False)
    h_acom: Mapped[int] = mapped_column(Integer, nullable=False)
    h_indep: Mapped[int] = mapped_column(Integer, nullable=False)
    idioma: Mapped[str] = mapped_column(String(45), nullable=False)
    espejo: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    entidad_espejo: Mapped[str] = mapped_column(String(45), nullable=False)
    pais_espejo: Mapped[str] = mapped_column(String(45), nullable=False)
    disenio: Mapped[Optional[int]] = mapped_column(Integer)

    programa: Mapped[Optional['Programa']] = relationship('Programa', back_populates='activ_academica')
    aa_rc: Mapped[List['AaRc']] = relationship('AaRc', back_populates='activ_academica')