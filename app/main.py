from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
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
from crud import (
    create_student,
    get_student_by_fio,
    get_students_by_group,
    get_all_students
)
from rules import (
    analyze_group,
    analyze_individual
)
from database import SessionLocal, engine, Base

app = FastAPI(
    title = 'Экспертная система: диагностика здоровья студентов'
)

app.add_middleware(
    CORSMiddleware,
    allow_origins = ['*'],
    allow_credentials = True,
    allow_methods = ['*'],
    allow_headers = ['*']
)


Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/students', response_model=StudentRead)
def create_student_endpoint(student: StudentCreate, db: Session = Depends(get_db)):
    existing = get_student_by_fio(db, student.fio)
    if existing:
        raise HTTPException(status_code=400, detail='Студент с таким ФИО уже существует')
    db_student = create_student(db, student)
    return db_student


@app.get('/students', response_model=list[StudentRead])
def list_students(db: Session = Depends(get_db)):
    return get_all_students(db)


@app.post('/analyze', response_model=AnalysisResult)
def analyze(fio: str | None = None, group: str | None = None, analyze_all: bool = False, db: Session = Depends(get_db)):
    # Определяем режим анализа
    if analyze_all:
        students = get_all_students(db)
        subject = 'Все'
    elif fio:
        stu = get_student_by_fio(db, fio)
        if not stu:
            raise HTTPException(status_code=404, detail='Студент не найден')
        students = [stu]
        subject = f'Студент: {fio}'
    elif group:
        students = get_students_by_group(db, group)
        if not students:
            raise HTTPException(status_code=404, detail='Группа не найдена или пустая')
        subject = f'Группа: {group}'
    else:
        raise HTTPException(status_code=400, detail='Укажите fio, group или analyze_all=true')
    
    # Если анализ группы (n>1) — агрегируем
    if len(students) > 1:
        n = len(students)
        total_missed = 0
        total_miss_dur = 0.0
        total_dorm = 0
        total_smoking = 0
        total_screen = 0.0
        total_phys = 0.0
        disease_counts = { 'respiratory':0, 'musculoskeletal':0, 'vision':0, 'gi':0, 'derm':0, 'mental':0, 'allergic':0, 'chronic':0 }

        for s in students:
            add = s.additional
            dis = s.diseases
            total_missed += (add.missed_lesson or 0)
            total_miss_dur += (add.avg_miss_duration or 0.0)
            total_dorm += 1 if (add.dorm) else 0
            total_smoking += 1 if (add.smoking) else 0
            total_screen += (add.screen_time or 0.0)
            total_phys += (add.physical_activity or 0.0)
            if dis.respiratory: disease_counts['respiratory'] += 1
            if dis.musculoskeletal: disease_counts['musculoskeletal'] += 1
            if dis.vision: disease_counts['vision'] += 1
            if dis.gi: disease_counts['gi'] += 1
            if dis.derm: disease_counts['derm'] += 1
            if dis.mental: disease_counts['mental'] += 1
            if dis.allergic: disease_counts['allergic'] += 1
            if dis.chronic: disease_counts['chronic'] += 1
    
        stats = {
                'n': n,
                'avg_missed_lesson': total_missed / n,
                'avg_miss_duration': total_miss_dur / n,
                'pct_dorm': total_dorm / n * 100,
                'pct_smoking': total_smoking / n * 100,
                'avg_screen_time': total_screen / n,
                'avg_physical_activity': total_phys / n,
                'disease_pct': { k: v / n * 100 for k, v in disease_counts.items() }
            }
        causes = analyze_group(stats)
        summary = f"Анализ {subject}, {n} студентов."
        return AnalysisResult(subject=subject, causes=[Cause(**c) for c in causes], summary=summary)
    else:
        # индивидуальный анализ
        s = students[0]
        student_dict = {
            'id': s.id,
            'fio': s.fio,
            'group': s.group,
            'additional': {
                'missed_lesson': s.additional.missed_lesson,
                'avg_miss_duration': s.additional.avg_miss_duration,
                'dorm': s.additional.dorm,
                'smoking': s.additional.smoking,
                'screen_time': s.additional.screen_time,
                'physical_activity': s.additional.physical_activity
            },
            'diseases': {
                'respiratory': s.diseases.respiratory,
                'musculoskeletal': s.diseases.musculoskeletal,
                'vision': s.diseases.vision,
                'gi': s.diseases.gi,
                'derm': s.diseases.derm,
                'mental': s.diseases.mental,
                'allergic': s.diseases.allergic,
                'chronic': s.diseases.chronic
            }
        }
        causes = analyze_individual(student_dict)
        summary = f"Индивидуальный анализ студента {s.fio}."
        return AnalysisResult(subject=subject, causes=[Cause(**c) for c in causes], summary=summary)

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(
#         'app.main',
#         host = '127.0.0.1',
#         port = 8000,
#         reload = True
#     )