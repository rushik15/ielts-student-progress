from datetime import date, datetime
from typing import Literal
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator, model_validator

Role = Literal["student", "teacher", "admin"]
Skill = Literal["listening", "reading", "writing"]


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int; student_number: str; full_name: str; email: str | None; role: Role; is_active: bool; teacher_id: int | None = None
    created_at: datetime | None = None


class LoginIn(BaseModel):
    student_number: str = Field(min_length=1, max_length=50)
    password: str = Field(min_length=1)


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


class PasswordChange(BaseModel):
    current_password: str = Field(min_length=4)
    new_password: str = Field(min_length=4, max_length=128)


class PasswordReset(BaseModel):
    new_password: str = Field(min_length=4, max_length=128)


class UserCreate(BaseModel):
    student_number: str = Field(min_length=1, max_length=50)
    full_name: str = Field(min_length=1, max_length=150)
    email: EmailStr | None = None
    password: str = Field(min_length=4, max_length=128)
    role: Role = "student"


class UserUpdate(BaseModel):
    full_name: str | None = Field(default=None, min_length=1, max_length=150)
    email: EmailStr | None = None
    is_active: bool | None = None


class MistakeIn(BaseModel):
    category: str | None = Field(default=None, max_length=100)
    question_reference: str | None = Field(default=None, max_length=100)
    description: str = Field(min_length=1)
    correction: str | None = None


class MistakeOut(MistakeIn):
    model_config = ConfigDict(from_attributes=True)
    id: int


class ScoreBase(BaseModel):
    skill: Skill
    writing_task: int | None = Field(default=None, ge=1, le=2)
    test_name: str = Field(min_length=1, max_length=200)
    test_date: date
    band_score: float = Field(ge=0, le=9)
    raw_score: int | None = Field(default=None, ge=0)
    total_questions: int | None = Field(default=None, gt=0)
    mistake_summary: str | None = None
    teacher_note: str | None = None

    @field_validator("band_score")
    @classmethod
    def half_bands_only(cls, value: float) -> float:
        if round(value * 2) != value * 2:
            raise ValueError("Band score must use 0.5 increments.")
        return value

    @model_validator(mode="after")
    def valid_raw_score(self):
        if self.raw_score is not None and self.total_questions is not None and self.raw_score > self.total_questions:
            raise ValueError("Raw score cannot exceed total questions.")
        return self

    @model_validator(mode="after")
    def writing_task_only_for_writing(self):
        if self.writing_task is not None and self.skill != "writing":
            raise ValueError("Writing task can only be used with Writing scores.")
        return self


class ScoreCreate(ScoreBase):
    mistakes: list[MistakeIn] = []


class ScoreUpdate(BaseModel):
    skill: Skill | None = None; writing_task: int | None = Field(default=None, ge=1, le=2); test_name: str | None = Field(default=None, min_length=1, max_length=200)
    test_date: date | None = None; band_score: float | None = Field(default=None, ge=0, le=9)
    raw_score: int | None = Field(default=None, ge=0); total_questions: int | None = Field(default=None, gt=0)
    mistake_summary: str | None = None; teacher_note: str | None = None

    @field_validator("band_score")
    @classmethod
    def half_bands_only(cls, value: float | None) -> float | None:
        if value is not None and round(value * 2) != value * 2:
            raise ValueError("Band score must use 0.5 increments.")
        return value


class ScoreOut(ScoreBase):
    model_config = ConfigDict(from_attributes=True)
    id: int; student_id: int; mistakes: list[MistakeOut] = []


class ProgressPoint(BaseModel):
    id: int; test_name: str; test_date: date; band_score: float


class ProgressOut(BaseModel):
    skill: Skill; latest: float | None; best: float | None; average: float | None; count: int; points: list[ProgressPoint]
