from pydantic import BaseModel, Field
from typing import Optional, List, Dict

class StudentDiseasesCreate(BaseModel):
    respiratory: bool = False
    musculoskeletal: bool = False
    vision: bool = False
    gi: bool = False
    derm: bool = False
    mental: bool = False
    allergic: bool = False
    chronic: bool = False


class AdditionalDataCreate(BaseModel):
    missed_lesson: int = 0
    avg_miss_duration: float = 0.0
    dorm: bool = False
    smoking: bool = False
    screen_time: float = 0.0
    physical_activity: float = 0.0


class StudentCreate(BaseModel):
    fio: str = Field(..., example='Иванов И.И.')
    group: str = Field(..., example='ПМИ-м-о-251')
    diseases: Optional[StudentDiseasesCreate] = StudentDiseasesCreate()
    additional: Optional[AdditionalDataCreate] = AdditionalDataCreate()


class StudentRead(BaseModel):
    id: int
    fio: str
    group: str

    class Config:
        orm_mode = True


class Cause(BaseModel):
    name: str
    confidence: float
    recommendation: str


class AnalysisResult(BaseModel):
    subject: str
    causes: List[Cause]
    summary: Optional[str] = None