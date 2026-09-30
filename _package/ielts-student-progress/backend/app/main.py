from contextlib import asynccontextmanager
from datetime import date
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import func, or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import inspect, text
from .config import get_settings
from .database import Base, engine, get_db
from .models import Mistake, ScoreRecord, User
from .schemas import (LoginIn, MistakeIn, MistakeOut, PasswordChange, PasswordReset, ProgressOut,
                      ScoreCreate, ScoreOut, ScoreUpdate, TokenOut, UserCreate, UserOut, UserUpdate)
from .security import create_access_token, decode_access_token, hash_password, verify_password

settings = get_settings()
bearer = HTTPBearer(auto_error=False)


def bootstrap_admin() -> None:
    with Session(engine) as db:
        existing = db.scalar(select(User).where(User.student_number == settings.bootstrap_admin_number))
        if not existing:
            db.add(User(student_number=settings.bootstrap_admin_number, full_name=settings.bootstrap_admin_name,
                        password_hash=hash_password(settings.bootstrap_admin_password), role="admin"))
            db.commit()


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    # Lightweight compatibility migration for existing local SQLite databases.
    if engine.dialect.name == "sqlite":
        columns = {column["name"] for column in inspect(engine).get_columns("users")}
        if "teacher_id" not in columns:
            with engine.begin() as connection:
                connection.execute(text("ALTER TABLE users ADD COLUMN teacher_id INTEGER REFERENCES users(id)"))
    bootstrap_admin()
    yield


app = FastAPI(title=settings.app_name, version="1.0.0", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=settings.origins, allow_credentials=False,
                   allow_methods=["*"], allow_headers=["Authorization", "Content-Type"])


def current_user(credentials: HTTPAuthorizationCredentials | None = Depends(bearer), db: Session = Depends(get_db)) -> User:
    if not credentials:
        raise HTTPException(status_code=401, detail="Authentication is required.")
    user = db.get(User, decode_access_token(credentials.credentials))
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="Session is invalid or the account is inactive.")
    return user


def teacher_user(user: User = Depends(current_user)) -> User:
    if user.role not in {"teacher", "admin"}:
        raise HTTPException(status_code=403, detail="Teacher or admin access is required.")
    return user


def get_student(student_id: int, db: Session, user: User) -> User:
    student = db.get(User, student_id)
    if not student or student.role != "student":
        raise HTTPException(status_code=404, detail="Student not found.")
    if user.role == "student" and user.id != student_id:
        raise HTTPException(status_code=403, detail="You cannot access another student's data.")
    if user.role == "teacher" and student.teacher_id != user.id:
        raise HTTPException(status_code=403, detail="This student is not assigned to you.")
    return student


def score_or_404(score_id: int, db: Session, user: User) -> ScoreRecord:
    score = db.scalar(select(ScoreRecord).options(selectinload(ScoreRecord.mistakes)).where(ScoreRecord.id == score_id))
    if not score:
        raise HTTPException(status_code=404, detail="Test record not found.")
    if user.role == "student" and score.student_id != user.id:
        raise HTTPException(status_code=403, detail="You cannot access another student's record.")
    if user.role == "teacher":
        student = db.get(User, score.student_id)
        if not student or student.teacher_id != user.id:
            raise HTTPException(status_code=403, detail="This student is not assigned to you.")
    return score


def serialize_score(score: ScoreRecord) -> ScoreOut:
    return ScoreOut.model_validate(score)


def progress_for(student_id: int, skill: str, db: Session) -> ProgressOut:
    records = list(db.scalars(select(ScoreRecord).where(ScoreRecord.student_id == student_id, ScoreRecord.skill == skill)
                              .order_by(ScoreRecord.test_date, ScoreRecord.created_at, ScoreRecord.id)))
    scores = [float(item.band_score) for item in records]
    return ProgressOut(skill=skill, latest=scores[-1] if scores else None, best=max(scores) if scores else None,
                       average=round(sum(scores) / len(scores), 1) if scores else None, count=len(scores),
                       points=[{"id": item.id, "test_name": item.test_name, "test_date": item.test_date, "band_score": float(item.band_score)} for item in records])


@app.exception_handler(IntegrityError)
async def integrity_error_handler(_, __):
    return __import__("fastapi").responses.JSONResponse(status_code=409, content={"detail": "A record with this student number or email already exists."})


@app.get("/api/v1/health", tags=["System"])
def health(): return {"status": "ok"}


@app.post("/api/v1/auth/login", response_model=TokenOut, tags=["Authentication"])
def login(payload: LoginIn, db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.student_number == payload.student_number))
    if not user or not user.is_active or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect student number or password.")
    return TokenOut(access_token=create_access_token(user.id), user=user)


@app.get("/api/v1/auth/me", response_model=UserOut, tags=["Authentication"])
def me(user: User = Depends(current_user)): return user


@app.post("/api/v1/auth/change-password", status_code=204, tags=["Authentication"])
def change_password(payload: PasswordChange, user: User = Depends(current_user), db: Session = Depends(get_db)):
    if not verify_password(payload.current_password, user.password_hash):
        raise HTTPException(status_code=400, detail="Current password is incorrect.")
    user.password_hash = hash_password(payload.new_password); db.commit()


@app.post("/api/v1/students", response_model=UserOut, status_code=201, tags=["Students"])
def create_student(payload: UserCreate, teacher: User = Depends(teacher_user), db: Session = Depends(get_db)):
    if payload.role != "student" and teacher.role != "admin":
        raise HTTPException(status_code=403, detail="Only an admin can create teacher accounts.")
    if db.scalar(select(User).where(or_(User.student_number == payload.student_number, User.email == payload.email if payload.email else False))):
        raise HTTPException(status_code=409, detail="Student number or email is already in use.")
    user = User(student_number=payload.student_number, full_name=payload.full_name, email=str(payload.email) if payload.email else None,
                password_hash=hash_password(payload.password), role=payload.role,
                teacher_id=teacher.id if payload.role == "student" and teacher.role == "teacher" else None)
    db.add(user); db.commit(); db.refresh(user); return user


@app.get("/api/v1/students", response_model=list[UserOut], tags=["Students"])
def list_students(search: str = "", current: User = Depends(teacher_user), db: Session = Depends(get_db)):
    query = select(User).where(User.role == "student")
    if current.role == "teacher":
        query = query.where(User.teacher_id == current.id)
    if search.strip():
        like = f"%{search.strip()}%"; query = query.where(or_(User.student_number.ilike(like), User.full_name.ilike(like)))
    return list(db.scalars(query.order_by(User.full_name).limit(200)))


@app.get("/api/v1/students/{student_id}", response_model=UserOut, tags=["Students"])
def student_detail(student_id: int, user: User = Depends(current_user), db: Session = Depends(get_db)):
    return get_student(student_id, db, user)


@app.patch("/api/v1/students/{student_id}", response_model=UserOut, tags=["Students"])
def update_student(student_id: int, payload: UserUpdate, user: User = Depends(current_user), db: Session = Depends(get_db)):
    student = get_student(student_id, db, user)
    if user.role == "student" and payload.is_active is not None:
        raise HTTPException(status_code=403, detail="Students cannot change account status.")
    for key, value in payload.model_dump(exclude_unset=True).items(): setattr(student, key, str(value) if key == "email" and value else value)
    try: db.commit()
    except IntegrityError: db.rollback(); raise HTTPException(status_code=409, detail="Email is already in use.")
    db.refresh(student); return student


@app.post("/api/v1/students/{student_id}/password", status_code=204, tags=["Students"])
def reset_password(student_id: int, payload: PasswordReset, teacher: User = Depends(teacher_user), db: Session = Depends(get_db)):
    student = get_student(student_id, db, teacher); student.password_hash = hash_password(payload.new_password); db.commit()


def create_score(student_id: int, payload: ScoreCreate, user: User, db: Session) -> ScoreOut:
    student = get_student(student_id, db, user)
    data = payload.model_dump(exclude={"mistakes"})
    if user.role == "student": data["teacher_note"] = None
    score = ScoreRecord(student_id=student.id, **data)
    score.mistakes = [Mistake(**mistake.model_dump()) for mistake in payload.mistakes]
    db.add(score); db.commit(); db.refresh(score)
    return serialize_score(score)


@app.post("/api/v1/scores", response_model=ScoreOut, status_code=201, tags=["Scores"])
def create_own_score(payload: ScoreCreate, user: User = Depends(current_user), db: Session = Depends(get_db)):
    if user.role != "student": raise HTTPException(status_code=400, detail="Teachers must select a student when creating a result.")
    return create_score(user.id, payload, user, db)


@app.post("/api/v1/students/{student_id}/scores", response_model=ScoreOut, status_code=201, tags=["Scores"])
def create_student_score(student_id: int, payload: ScoreCreate, teacher: User = Depends(teacher_user), db: Session = Depends(get_db)):
    return create_score(student_id, payload, teacher, db)


@app.get("/api/v1/scores", response_model=list[ScoreOut], tags=["Scores"])
def list_scores(student_id: int | None = None, skill: str | None = None, user: User = Depends(current_user), db: Session = Depends(get_db)):
    target_id = user.id if user.role == "student" else student_id
    if target_id is None: raise HTTPException(status_code=400, detail="student_id is required for teacher requests.")
    get_student(target_id, db, user)
    query = select(ScoreRecord).options(selectinload(ScoreRecord.mistakes)).where(ScoreRecord.student_id == target_id)
    if skill: query = query.where(ScoreRecord.skill == skill)
    return list(db.scalars(query.order_by(ScoreRecord.test_date.desc(), ScoreRecord.created_at.desc())))


@app.get("/api/v1/scores/{score_id}", response_model=ScoreOut, tags=["Scores"])
def get_score(score_id: int, user: User = Depends(current_user), db: Session = Depends(get_db)): return score_or_404(score_id, db, user)


@app.patch("/api/v1/scores/{score_id}", response_model=ScoreOut, tags=["Scores"])
def update_score(score_id: int, payload: ScoreUpdate, user: User = Depends(current_user), db: Session = Depends(get_db)):
    score = score_or_404(score_id, db, user); updates = payload.model_dump(exclude_unset=True)
    if user.role == "student": updates.pop("teacher_note", None)
    merged = {**{key: getattr(score, key) for key in ["raw_score", "total_questions"]}, **updates}
    if merged["raw_score"] is not None and merged["total_questions"] is not None and merged["raw_score"] > merged["total_questions"]:
        raise HTTPException(status_code=422, detail="Raw score cannot exceed total questions.")
    for key, value in updates.items(): setattr(score, key, value)
    db.commit(); db.refresh(score); return score


@app.delete("/api/v1/scores/{score_id}", status_code=204, tags=["Scores"])
def delete_score(score_id: int, user: User = Depends(current_user), db: Session = Depends(get_db)):
    score = score_or_404(score_id, db, user); db.delete(score); db.commit()


@app.post("/api/v1/scores/{score_id}/mistakes", response_model=MistakeOut, status_code=201, tags=["Mistakes"])
def add_mistake(score_id: int, payload: MistakeIn, user: User = Depends(current_user), db: Session = Depends(get_db)):
    score = score_or_404(score_id, db, user); mistake = Mistake(score_record_id=score.id, **payload.model_dump()); db.add(mistake); db.commit(); db.refresh(mistake); return mistake


@app.get("/api/v1/scores/{score_id}/mistakes", response_model=list[MistakeOut], tags=["Mistakes"])
def list_mistakes(score_id: int, user: User = Depends(current_user), db: Session = Depends(get_db)):
    score = score_or_404(score_id, db, user); return score.mistakes


@app.get("/api/v1/progress/{skill}", response_model=ProgressOut, tags=["Progress"])
def own_progress(skill: str, user: User = Depends(current_user), db: Session = Depends(get_db)):
    if skill not in {"listening", "reading", "writing"}: raise HTTPException(status_code=422, detail="Invalid skill.")
    if user.role != "student": raise HTTPException(status_code=400, detail="Teachers must select a student.")
    return progress_for(user.id, skill, db)


@app.get("/api/v1/students/{student_id}/progress/{skill}", response_model=ProgressOut, tags=["Progress"])
def student_progress(student_id: int, skill: str, teacher: User = Depends(teacher_user), db: Session = Depends(get_db)):
    if skill not in {"listening", "reading", "writing"}: raise HTTPException(status_code=422, detail="Invalid skill.")
    get_student(student_id, db, teacher); return progress_for(student_id, skill, db)


@app.get("/api/v1/dashboard/teacher", tags=["Dashboard"])
def teacher_dashboard(_: User = Depends(teacher_user), db: Session = Depends(get_db)):
    students = db.scalar(select(func.count()).select_from(User).where(User.role == "student")) or 0
    tests = db.scalar(select(func.count()).select_from(ScoreRecord)) or 0
    recent = list(db.scalars(select(User).where(User.role == "student").order_by(User.updated_at.desc()).limit(8)))
    return {"total_students": students, "total_tests": tests, "recent_students": [UserOut.model_validate(item).model_dump(mode="json") for item in recent]}
