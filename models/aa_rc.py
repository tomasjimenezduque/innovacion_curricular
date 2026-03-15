from sqlalchemy import String, Integer, ForeignKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

class AaRc(Base):
    __tablename__ = 'aa_rc'
    __table_args__ = (
        ForeignKeyConstraint(['activ_academicas_idcurso'], ['activ_academica.id'], name='aa_rc_activ_academicas_idcurso_fkey'),
        ForeignKeyConstraint(['registro_calificado_codigo'], ['registro_calificado.codigo'], name='aa_rc_registro_calificado_codigo_fkey'),
    )

    activ_academicas_idcurso: Mapped[int] = mapped_column(Integer, primary_key=True)
    registro_calificado_codigo: Mapped[int] = mapped_column(Integer, primary_key=True)
    componente: Mapped[str] = mapped_column(String(45), nullable=False)
    semestre: Mapped[str] = mapped_column(String(45), nullable=False)

    activ_academica: Mapped['ActivAcademica'] = relationship('ActivAcademica', back_populates='aa_rc')
    registro_calificado: Mapped['RegistroCalificado'] = relationship('RegistroCalificado', back_populates='aa_rc')