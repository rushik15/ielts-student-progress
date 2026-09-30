from datetime import date, datetime
from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .database import Base


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    student_number: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    full_name: Mapped[str] = mapped_column(String(150), index=True)
    email: Mapped[str | None] = mapped_column(String(255), unique=True, nullable=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(20), default="student", index=True)
    teacher_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True, index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    scores: Mapped[list["ScoreRecord"]] = relationship(back_populates="student", cascade="all, delete-orphan")
    teacher: Mapped["User | None"] = relationship(remote_side="User.id", foreign_keys=[teacher_id], backref="assigned_students")


class ScoreRecord(Base):
    __tablename__ = "score_records"
    id: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    skill: Mapped[str] = mapped_column(String(20), index=True)
    writing_task: Mapped[int | None] = mapped_column(Integer, nullable=True)
    test_name: Mapped[str] = mapped_column(String(200))
    test_date: Mapped[date] = mapped_column(Date, index=True)
    band_score: Mapped[float] = mapped_column(Numeric(2, 1))
    raw_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    total_questions: Mapped[int | None] = mapped_column(Integer, nullable=True)
    mistake_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    teacher_note: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    student: Mapped[User] = relationship(back_populates="scores")
    mistakes: Mapped[list["Mistake"]] = relationship(back_populates="score", cascade="all, delete-orphan")


class Mistake(Base):
    __tablename__ = "mistakes"
    id: Mapped[int] = mapped_column(primary_key=True)
    score_record_id: Mapped[int] = mapped_column(ForeignKey("score_records.id", ondelete="CASCADE"), index=True)
    category: Mapped[str | None] = mapped_column(String(100), nullable=True)
    question_reference: Mapped[str | None] = mapped_column(String(100), nullable=True)
    description: Mapped[str] = mapped_column(Text)
    correction: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    score: Mapped[ScoreRecord] = relationship(back_populates="mistakes")
