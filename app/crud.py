from sqlalchemy.orm import Session
from models import (
    Student,
    StudentDiseases,
    AdditionalData
)
from schemas import (
    StudentDiseasesCreate,
    AdditionalDataCreate,
    StudentCreate,
    StudentRead,
    Cause,
    AnalysisResult
)


def create_student(db: Session, student: StudentCreate):
    db_student = Student(
        fio = student.fio,
        group = student.group
    )

    db_student.diseases = StudentDiseases(**student.diseases.dict())
    db_student.additional = AdditionalData(**student.additional.dict())

    db.add(db_student)
    db.commit()
    db.refresh(db_student)

    return db_student


def get_student_by_fio(db: Session, fio: str):
    return db.query(Student).filter(
        Student.fio == fio
    ).first()


def get_students_by_group(db: Session, group: str):
    return db.query(Student).filter(
        Student.group == group
    ).all()


def get_all_students(db: Session):
    return db.query(Student).all()


