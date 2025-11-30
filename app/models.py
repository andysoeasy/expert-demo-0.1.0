from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Float,
    ForeignKey
)
from sqlalchemy.orm import relationship
from database import Base

class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key = True, index = True)
    fio = Column(String, nullable = False, index = True)
    group = Column(String, nullable = False, index = True)

    diseases = relationship(
        'StudentDiseases',
        uselist = False,
        back_populates = 'student',
        cascade = 'all, delete-orphan'
    )

    additional = relationship(
        'AdditionalData',
        uselist = False,
        back_populates = False,
        cascade = 'all, delete-orphan'
    )


class StudentDiseases(Base):
    __tablename__ = 'diseases_students'
    id = Column(Integer, ForeignKey('students.id'), primary_key = True)
    respiratory = Column(Boolean, default = False)
    musculoskeletal = Column(Boolean, default = False)
    vision = Column(Boolean, default = False)
    gi = Column(Boolean, default = False)
    derm = Column(Boolean, default = False)
    mental = Column(Boolean, default = False)
    allergic = Column(Boolean, default = False)
    chronic = Column(Boolean, default = False)

    student = relationship(
        'Student',
        back_populates = 'diseases'
    )


class AdditionalData(Base):
    __tablename__ = 'additional_data'
    id = Column(Integer, ForeignKey('students.id'), primary_key = True)
    missed_lesson = Column(Integer, default = 0)
    avg_miss_duration = Column(Float, default = 0)
    dorm = Column(Boolean, default = False)
    smoking = Column(Boolean, default = False)
    screen_time = Column(Float, default = 0.0)
    physical_activity = Column(Float, default = 0.0)

    student = relationship(
        'Student',
        back_populates = 'additional'
    )
