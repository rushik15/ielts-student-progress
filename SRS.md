# IELTS Student Progress Portal
## Full-Stack Software Requirements Specification (SRS) + Codex Build Specification

**Document version:** 2.0  
**Date:** 30 September 2026  
**Target build tool:** OpenAI Codex  
**Starting codebase:** `IELTS_Student_Progress_Backend_MVP.zip`  
**Product type:** Full-stack web application  

---

# 1. Codex Mission

Transform the supplied backend-only ZIP into a **complete, production-ready full-stack IELTS Student Progress Portal**.

The final project must contain:

1. A Python FastAPI backend.
2. A React + Vite + TypeScript frontend.
3. A Student Portal.
4. A Teacher/Admin Portal.
5. PostgreSQL support for production.
6. SQLite support for simple local development.
7. Authentication and role-based authorization.
8. Test-score and mistake tracking for IELTS Listening, Reading and Writing.
9. Separate progress graphs for Listening, Reading and Writing.
10. Responsive desktop/tablet/mobile UI.
11. Automated backend and frontend validation/tests.
12. Local one-command startup for Windows and a simple command for macOS/Linux.
13. Production deployment files and instructions.
14. A final ZIP containing the **entire project**, not just the backend.

The application should be simple enough for a teacher with limited technical knowledge to run locally and deploy online with minimal configuration.

---

# 2. Critical Codex Instructions

These instructions are mandatory.

## 2.1 Preserve the existing backend

The current ZIP already contains a working FastAPI backend for:

- authentication,
- students,
- scores,
- mistakes,
- progress,
- teacher dashboard,
- SQLite/PostgreSQL connectivity,
- JWT authentication.

Read the existing backend before changing it. Reuse working code wherever practical instead of rewriting everything.

## 2.2 Do not break existing API behaviour unnecessarily

Existing endpoints that already work should remain compatible unless a change is required for a frontend requirement or security fix.

When an endpoint must change, update:

- Pydantic schemas,
- frontend API client,
- tests,
- README,
- OpenAPI documentation,
- environment examples,

so the project remains internally consistent.

## 2.3 Do not ask for clarification

Use the assumptions in this SRS as the source of truth. Do not stop the implementation because a small product decision was not explicitly stated.

## 2.4 No fake functionality

Do not create buttons that do nothing.

Every visible feature must either work end-to-end or be clearly labelled as unavailable. For the MVP, prefer removing unnecessary UI over leaving unfinished controls.

## 2.5 No invented IELTS results

The system must display only data entered into the database. Never generate, estimate, or fabricate a student's band score or mistakes.

## 2.6 Validate all inputs

Validation must exist in both frontend and backend. Backend validation is authoritative.

## 2.7 Final build must be runnable

Before finishing:

- run backend syntax checks,
- run backend tests,
- build the frontend,
- run frontend tests/lint/type-check where configured,
- verify the frontend can communicate with the backend,
- verify login for Student and Teacher/Admin,
- verify score creation,
- verify mistake creation,
- verify progress graph data,
- verify role-based access,
- verify production environment variables are documented.

---

# 3. Product Vision

Teachers need a simple way to track IELTS practice performance over time.

A student logs in using a student number and password. The student can enter a test record for Listening, Reading or Writing. Each record contains the test name, date, band score and mistakes. The student can then see the history and progress of each skill in a graph.

Teachers have a separate portal where they can see all students, search students, open an individual student's dashboard, review test history and mistakes, and optionally enter or edit results for a student.

The application is an educational progress tracker. It is not an official IELTS scoring or certification system.

---

# 4. Roles

## 4.1 Student

A Student can:

- log in with student number and password,
- view own profile,
- change own password,
- add own Listening result,
- add own Reading result,
- add own Writing result,
- add mistakes to each test,
- edit own result,
- delete own result,
- view own test history,
- view separate progress graphs,
- see latest, best and average band for each skill,
- see mistakes belonging to their own tests.

A Student must never be able to view another student's private data.

## 4.2 Teacher

A Teacher can:

- log in,
- view teacher dashboard,
- view student list,
- search students by student number or name,
- open an individual student,
- view all three skill progress graphs for that student,
- view test history,
- view mistakes,
- create a score record for a student,
- edit a score record for a student,
- delete a score record for a student,
- optionally add teacher notes,
- update student profile fields allowed by the backend,
- reset a student's password.

## 4.3 Admin

Admin is an elevated role that uses the Teacher/Admin portal.

Admin can perform all Teacher actions and can additionally:

- create teacher accounts,
- deactivate/reactivate users when implemented,
- manage the initial portal configuration.

The MVP may keep Admin-only controls minimal. Do not build an unnecessary complex administration system.

---

# 5. Recommended Technology Stack

Use boring, stable, well-supported technologies rather than adding unnecessary dependencies.

## 5.1 Frontend

- React
- Vite
- TypeScript
- React Router
- Recharts for graphs
- Native `fetch` or a very small API client layer
- CSS modules, plain CSS, or a simple utility approach
- Avoid a large UI framework unless it materially reduces complexity

The frontend must build as a static SPA.

## 5.2 Backend

Keep the existing backend stack:

- Python
- FastAPI
- SQLAlchemy 2.x
- Pydantic / pydantic-settings
- JWT
- PostgreSQL for production
- SQLite for local development
- Uvicorn

Use Alembic for production-safe database migrations if practical. Do not make migrations so complex that the application stops being easy to run locally.

## 5.3 Testing

Backend:

- pytest
- FastAPI TestClient or equivalent

Frontend:

- TypeScript compiler
- build validation
- lightweight component/API tests where practical

---

# 6. Final Repository Structure

Codex should produce this approximate structure:

```text
ielts-student-progress/
│
├── backend/
│   ├── app/
│   ├── tests/
│   ├── migrations/                 # when Alembic is used
│   ├── requirements.txt
│   ├── pyproject.toml
│   ├── Dockerfile
│   ├── .env.example
│   └── README.md
│
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   ├── auth/
│   │   ├── components/
│   │   ├── layouts/
│   │   ├── pages/
│   │   ├── charts/
│   │   ├── types/
│   │   ├── utils/
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── public/
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   ├── .env.example
│   ├── vercel.json               # or equivalent SPA deployment config
│   └── README.md
│
├── scripts/
│   ├── run.bat
│   ├── run.ps1
│   └── stop.bat
│
├── docker-compose.yml             # optional but preferred for local full-stack run
├── render.yaml                    # backend deployment configuration
├── README.md                      # complete root documentation
├── SRS.md                        # this specification
└── .gitignore
```

The exact filenames may vary slightly, but frontend and backend must be clearly separated.

---

# 7. Core Business Rules

## 7.1 Skills

The MVP supports exactly these three IELTS skills:

- Listening
- Reading
- Writing

Do not add Speaking to the main UI unless explicitly requested later.

## 7.2 Band score

Band score:

- minimum: 0.0,
- maximum: 9.0,
- increment: 0.5.

Valid examples:

- 5.0
- 5.5
- 6.0
- 6.5
- 7.0
- 8.5
- 9.0

Invalid examples:

- 6.2
- 7.25
- 9.5
- -1

## 7.3 Raw score

Raw score and total questions are optional.

They are primarily useful for Listening and Reading.

For Writing, the frontend should not force a 40-question raw score.

If raw score and total questions are both supplied, raw score must not exceed total questions.

## 7.4 Test name

Required.

Examples:

- Cambridge 19 Test 1
- Weekly Mock Test 03
- Writing Task 2 Practice 07
- Full Reading Mock – September 2026

Do not force a fixed Cambridge test naming pattern.

## 7.5 Test date

Required in the final stored record.

If omitted by the user, backend may default to the current date.

## 7.6 Mistakes

A test may contain zero or more mistakes.

Each mistake may contain:

- category,
- question reference,
- description,
- correction.

The description is required.

Examples of optional categories:

Listening:
- spelling
- plural/singular
- distractor
- number/date
- map/diagram
- multiple choice
- form completion
- misunderstanding

Reading:
- vocabulary
- paraphrase
- True/False/Not Given
- Yes/No/Not Given
- heading matching
- information matching
- multiple choice
- summary completion
- careless mistake

Writing:
- grammar
- vocabulary
- spelling
- task response
- coherence/cohesion
- sentence structure
- article/preposition
- word choice

These are suggestions only. The database may store free-text categories so teachers can use categories not listed above.

## 7.7 Teacher note

Teacher notes are optional and are visible to teachers/admins. Student visibility must be explicitly decided in the frontend. For MVP, display teacher notes to the student only if the UI labels them as teacher feedback; otherwise keep them teacher-only.

---

# 8. Authentication Requirements

## Login

Single login page with:

- Student Number / User ID
- Password
- Login button

The same login API can authenticate Students, Teachers and Admins.

After successful login:

- Student → Student Portal
- Teacher/Admin → Teacher/Admin Portal

## Authentication storage

The existing API uses JWT bearer tokens.

For the MVP, the frontend may persist the token in browser storage, but implement:

- token existence check,
- current-user fetch on application startup,
- automatic logout when API returns 401,
- clear token on logout,
- protected routes.

Do not log tokens or passwords.

## Password rules

Minimum length: 4 characters for compatibility with the existing backend.

Frontend should recommend a stronger password when the user changes it, but should not contradict backend validation.

---

# 9. Student Portal Requirements

## 9.1 Student Layout

Desktop layout:

- left sidebar or top navigation,
- main content area,
- account/logout control.

Mobile:

- collapsible menu or top menu,
- no horizontal scrolling,
- cards stack vertically.

## 9.2 Student Dashboard

The dashboard should show:

### Welcome section

- student full name,
- student number,
- quick action to add a test.

### Skill summary cards

One card each for:

- Listening
- Reading
- Writing

Each card displays when data exists:

- Latest band
- Best band
- Average band
- Number of tests

When no records exist:

- show `No tests recorded yet`.

### Progress charts

Display three clear line charts:

- Listening Progress
- Reading Progress
- Writing Progress

Each graph must use the student's stored records only.

Suggested axes:

- X-axis: date/test order
- Y-axis: band score from 0 to 9

Tooltips should show:

- test name,
- date,
- band score.

## 9.3 Add Test

Use a dedicated page or modal.

Fields:

1. Skill
2. Test name
3. Test date
4. Band score
5. Raw score (optional)
6. Total questions (optional)
7. Mistake summary (optional)
8. Teacher note/feedback area only when permitted
9. Repeatable mistake rows

Each mistake row:

- category
- question reference
- description
- correction
- remove row

Buttons:

- Add Mistake
- Save Test
- Cancel

After save:

- show success message,
- return to score history or dashboard,
- refresh chart data automatically.

## 9.4 Score History

Table/cards showing:

- skill,
- test name,
- date,
- band score,
- raw score when present,
- number of mistakes,
- actions.

Actions:

- View
- Edit
- Delete

Include a confirmation before delete.

## 9.5 Test Detail

Show:

- test information,
- band score,
- raw score / total,
- mistake summary,
- all individual mistakes,
- correction notes,
- teacher feedback if applicable.

---

# 10. Teacher/Admin Portal Requirements

## 10.1 Teacher Dashboard

Show:

- total students,
- total recorded tests,
- students with recent activity,
- searchable student list.

Student table columns:

- student number,
- full name,
- email if available,
- tests recorded,
- last test date,
- open button.

## 10.2 Student Search

Search by:

- student number,
- student name.

Search should call the backend search parameter rather than downloading huge datasets when practical.

## 10.3 Student Detail

When a teacher opens a student:

Header:

- name,
- student number,
- email,
- account status.

Summary:

- Listening latest/best/average/tests,
- Reading latest/best/average/tests,
- Writing latest/best/average/tests.

Charts:

- Listening,
- Reading,
- Writing.

History:

- all records,
- skill filter,
- date ordering.

Mistakes:

- expandable test rows/cards,
- mistake category,
- description,
- correction.

Teacher actions:

- Add Result
- Edit Student
- Reset Password

## 10.4 Add Result for Student

Teacher may create a test on behalf of a student.

Use the same fields and validation as the Student Add Test screen.

## 10.5 Teacher Notes

Teacher may add structured feedback to a test.

The backend field already exists as `teacher_note`.

The frontend must handle this field consistently.

---

# 11. Profile Requirements

## Student profile

Show:

- full name,
- student number,
- email,
- role,
- account status.

Allow:

- edit permitted profile fields,
- change password,
- logout.

## Teacher/Admin profile

Show the same account basics.

Allow password change.

Do not expose password hashes, JWTs or security internals.

---

# 12. Pages / Routes

Recommended frontend routes:

```text
/login

/student
/student/dashboard
/student/tests
/student/tests/new
/student/tests/:scoreId
/student/tests/:scoreId/edit
/student/profile

/teacher
/teacher/dashboard
/teacher/students
/teacher/students/:studentId
/teacher/students/:studentId/tests/new
/teacher/profile
```

The exact route aliases may be simplified, but role separation must remain clear.

Protected-route rules:

- Student routes require role `student`.
- Teacher routes require role `teacher` or `admin`.
- Unauthenticated users go to `/login`.
- Authenticated users should not see `/login` except after logout.

---

# 13. Frontend Components

Create reusable components rather than duplicating UI code.

Recommended components:

```text
Navbar / Sidebar
ProtectedRoute
RoleRoute
LoadingSpinner
ErrorMessage
EmptyState
Toast / Alert
SkillCard
SkillBadge
ScoreForm
MistakeFormRow
MistakeList
ScoreTable
ScoreCard
ScoreDetail
ProgressChart
ProgressChartPanel
StudentTable
StudentSearch
StudentSummary
ConfirmDialog
PasswordForm
```

Charts should be reusable with a skill parameter.

---

# 14. API Integration

Create one central API client.

The frontend must not scatter raw API URLs across dozens of components.

Use an environment variable such as:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000/api/v1
```

Production example:

```env
VITE_API_BASE_URL=https://YOUR-BACKEND-DOMAIN/api/v1
```

The exact production URL must be supplied through deployment environment settings, not hard-coded into source code.

## Existing API contract to preserve/use

### Authentication

```http
POST /api/v1/auth/login
GET  /api/v1/auth/me
POST /api/v1/auth/change-password
```

### Students

```http
POST  /api/v1/students
GET   /api/v1/students?search=<query>
GET   /api/v1/students/{student_id}
PATCH /api/v1/students/{student_id}
POST  /api/v1/students/{student_id}/password
```

### Scores

```http
POST   /api/v1/scores
POST   /api/v1/students/{student_id}/scores
GET    /api/v1/scores
GET    /api/v1/scores/{score_id}
PATCH  /api/v1/scores/{score_id}
DELETE /api/v1/scores/{score_id}
```

### Mistakes

```http
POST /api/v1/scores/{score_id}/mistakes
GET  /api/v1/scores/{score_id}/mistakes
```

### Progress

```http
GET /api/v1/progress/{skill}
GET /api/v1/students/{student_id}/progress/{skill}
```

Where `{skill}` is:

```text
listening
reading
writing
```

### Dashboard / health

```http
GET /api/v1/dashboard/teacher
GET /api/v1/health
```

If the existing backend provides an equivalent endpoint instead of exactly one listed above, adapt the frontend to the actual response and keep documentation synchronized.

---

# 15. Backend Enhancements Required for Full Project

The existing backend is the starting point, but Codex must inspect and enhance it where necessary.

Required improvements:

1. Add or complete teacher account creation/management if the current API cannot provision teachers.
2. Ensure teachers cannot access arbitrary users outside the intended role model.
3. Enforce that Students can access only their own records.
4. Ensure score update/delete authorization is correct.
5. Ensure mistake authorization is correct.
6. Validate that raw score does not exceed total questions.
7. Add database migrations if production deployment needs schema evolution.
8. Improve error responses so the frontend can show useful messages.
9. Enable proper CORS based on `CORS_ORIGINS`.
10. Keep secrets in environment variables.
11. Do not expose stack traces or SQL errors to end users in production.
12. Add indexes for common lookups.
13. Return consistent JSON error responses.
14. Add/update automated API tests.

---

# 16. Data Model

## Users

```text
id                integer PK
student_number    varchar(50) UNIQUE NOT NULL
full_name         varchar(150) NOT NULL
email             varchar(255) UNIQUE NULL
password_hash     varchar(255) NOT NULL
role              student | teacher | admin
is_active         boolean NOT NULL DEFAULT true
created_at        datetime
updated_at        datetime
```

## Score Records

```text
id                 integer PK
student_id         FK -> users.id
skill              listening | reading | writing
test_name          varchar(200)
test_date          date
band_score         numeric(2,1)
raw_score          integer NULL
total_questions    integer NULL
mistake_summary    text NULL
teacher_note       text NULL
created_at         datetime
updated_at         datetime
```

## Mistakes

```text
id                    integer PK
score_record_id       FK -> score_records.id
category              varchar(100) NULL
question_reference    varchar(100) NULL
description           text NOT NULL
correction            text NULL
created_at            datetime
```

Relationship:

```text
User 1 ---- N ScoreRecord
ScoreRecord 1 ---- N Mistake
```

Deleting a score should cascade to its mistakes.

Deleting a student should cascade to their score records and mistakes, subject to any safety protections Codex introduces.

---

# 17. Progress Calculation

For each skill:

### Latest band

Band score from the most recent test date. If dates are equal, use the newest record.

### Best band

Maximum stored band score.

### Average band

Arithmetic mean of all stored band scores for that skill.

Display average rounded to one decimal place.

### Total tests

Number of records for that skill.

### Graph

Plot each recorded test in chronological order.

Do not smooth, interpolate, or invent missing points.

---

# 18. UI / UX Requirements

The design should look like a clean modern education dashboard, not a complicated enterprise system.

Suggested visual hierarchy:

- clear header,
- calm neutral background,
- white cards,
- strong readable headings,
- obvious action button,
- simple charts,
- consistent spacing,
- accessible form labels.

Do not overdesign the application.

Prioritize:

1. readability,
2. speed of entering a result,
3. easy progress tracking,
4. teacher student lookup.

## Empty states

Examples:

- `No Listening tests recorded yet.`
- `No Reading tests recorded yet.`
- `No Writing tests recorded yet.`
- `No mistakes recorded for this test.`

## Error states

Examples:

- invalid credentials,
- duplicate student number,
- server unavailable,
- validation error,
- expired session.

Use human-readable messages.

## Loading states

Show loading indicators while:

- logging in,
- loading dashboard,
- loading students,
- saving a score,
- updating a student.

Disable duplicate submission while a form is being saved.

---

# 19. Accessibility

Minimum requirements:

- semantic buttons and labels,
- keyboard-accessible controls,
- visible focus states,
- sufficient text contrast,
- charts accompanied by textual summary/stat cards,
- form validation messages associated with their fields,
- responsive mobile layout.

Do not rely on colour alone to communicate an important state.

---

# 20. Security

Required:

- passwords stored only as hashes,
- JWT secret from environment variable,
- CORS restricted to configured frontend origin(s),
- no credentials in source code,
- no password/token logging,
- role-based route protection,
- object-level authorization on every student/score/mistake resource,
- backend validation for all mutable data,
- production HTTPS assumed at hosting layer,
- clear logout behaviour,
- do not return password hashes in API responses.

For production, use a strong randomly generated `SECRET_KEY`.

---

# 21. Environment Variables

## Backend `.env.example`

```env
APP_NAME=IELTS Student Progress Portal API
SECRET_KEY=replace-with-a-long-random-secret
ACCESS_TOKEN_EXPIRE_MINUTES=1440
DATABASE_URL=sqlite:///./ielts_progress.db
CORS_ORIGINS=http://localhost:5173

BOOTSTRAP_ADMIN_NUMBER=admin001
BOOTSTRAP_ADMIN_PASSWORD=change-me-now
BOOTSTRAP_ADMIN_NAME=Portal Admin
```

Production should use PostgreSQL, for example:

```env
DATABASE_URL=postgresql+psycopg://USER:PASSWORD@HOST:5432/DATABASE
```

Do not commit real credentials.

## Frontend `.env.example`

```env
VITE_API_BASE_URL=http://127.0.0.1:8000/api/v1
```

---

# 22. Local Development Requirements

The project must be runnable on Windows because the intended user environment may be Windows.

## Backend

```bat
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

## Frontend

```bat
cd frontend
npm install
npm run dev
```

Default development URLs:

```text
Frontend: http://localhost:5173
Backend:  http://127.0.0.1:8000
Docs:     http://127.0.0.1:8000/docs
Health:   http://127.0.0.1:8000/api/v1/health
```

---

# 23. One-Command Windows Startup

Create:

```text
scripts/run.bat
```

The script should:

1. verify Python exists,
2. verify Node/npm exists,
3. create backend virtual environment if missing,
4. install backend requirements when needed,
5. install frontend packages when `node_modules` is missing,
6. start the FastAPI backend,
7. start the Vite frontend,
8. print the URLs.

Create:

```text
scripts/stop.bat
```

which stops the development processes started by the script.

Also provide:

```text
scripts/run.ps1
```

for PowerShell users.

The scripts should fail with a clear message instead of silently doing nothing.

---

# 24. Deployment Architecture

Use a simple split deployment:

```text
Browser
  |
  v
React/Vite frontend
  |
  | HTTPS REST API
  v
FastAPI backend
  |
  v
PostgreSQL database
```

Recommended deployment categories:

- Frontend: static hosting such as Vercel or Netlify.
- Backend: Render or another Docker/Python host.
- Database: managed PostgreSQL such as Supabase or another persistent PostgreSQL provider.

The application must not depend on a local laptop after deployment.

## Important persistence rule

Do not use SQLite as the production database when the hosting filesystem is ephemeral.

Use PostgreSQL in production.

---

# 25. Production Deployment Files

Codex should supply:

## Backend Dockerfile

A production-capable Dockerfile that:

- installs dependencies,
- starts Uvicorn,
- binds to `0.0.0.0`,
- respects platform `PORT`.

## Render configuration

Provide `render.yaml` or equivalent configuration for the backend.

Required environment variables should be explicitly documented.

## Frontend deployment

Provide the configuration needed for SPA fallback so refreshing routes such as:

```text
/student/dashboard
/teacher/students/12
```

does not return a hosting 404.

The frontend must read `VITE_API_BASE_URL` from deployment environment variables.

---

# 26. CORS

The backend must accept requests from the deployed frontend origin.

Local development should allow:

```text
http://localhost:5173
```

and/or:

```text
http://127.0.0.1:5173
```

Production origins should be explicitly configured through `CORS_ORIGINS`.

Do not use unrestricted wildcard CORS with credentials in production.

---

# 27. Database Startup / Migration Behaviour

Local SQLite should work with minimal setup.

Production PostgreSQL schema should be created/migrated predictably.

If Alembic is implemented:

```bash
alembic upgrade head
```

must be documented.

The startup process must not unexpectedly destroy existing data.

Never use a destructive `drop_all()` operation during normal startup.

---

# 28. Error Handling Contract

Use consistent API responses.

For validation errors, return a structure that the frontend can map to fields when practical.

For authentication failures:

```text
401 Unauthorized
```

For forbidden resources:

```text
403 Forbidden
```

For missing resources:

```text
404 Not Found
```

For duplicate student numbers/emails:

```text
409 Conflict
```

For unexpected failures:

```text
500 Internal Server Error
```

Never expose internal exception traces to ordinary users.

---

# 29. Backend API Quality Requirements

Add appropriate pagination later, but the MVP may retain a sensible maximum result limit for simplicity.

The teacher dashboard should avoid N+1 database patterns where reasonably easy.

All endpoints must have useful Swagger/OpenAPI descriptions.

Use typed Python models and response schemas.

Avoid global mutable state other than application configuration and database engine/session management.

---

# 30. Frontend State Management

Do not introduce Redux unless necessary.

For this application, local React state plus a small authentication context/provider is sufficient.

Recommended:

```text
AuthContext
  -> currentUser
  -> token
  -> login()
  -> logout()
  -> refreshCurrentUser()
```

Page-level data fetching should be simple and explicit.

Avoid overengineering caching.

---

# 31. Forms

Every form must have:

- labels,
- required markers where appropriate,
- client validation,
- backend validation handling,
- disabled submit during save,
- success feedback,
- useful error feedback.

Score form band selector should make 0.0–9.0 half-band values easy to select.

Use a select or controlled numeric input that cannot easily produce invalid decimals.

Mistake rows should support adding multiple mistakes in one test submission.

---

# 32. Graph Requirements

Use line charts.

Do not visually compare different students on the Student Portal.

Teacher Student Detail pages may show all three skill graphs for the selected student.

Graph requirements:

- Y-axis minimum 0,
- Y-axis maximum 9,
- clearly labelled skill,
- tooltip with test name/date/band,
- responsive width,
- readable axis labels,
- empty state when no data exists.

The chart and summary statistics must be based on the same source data.

---

# 33. Sample Student Workflow

1. Student opens `/login`.
2. Student enters student number and password.
3. Backend authenticates.
4. Frontend calls `/auth/me`.
5. Frontend sees role `student`.
6. Frontend redirects to Student Dashboard.
7. Student clicks `Add Test`.
8. Student selects `Listening`.
9. Student enters `Cambridge 19 Test 1`.
10. Student enters date and band `6.5`.
11. Student enters optional raw score `30/40`.
12. Student adds mistakes such as spelling or distractor errors.
13. Student saves.
14. Frontend refreshes progress.
15. Listening graph displays the new point.
16. Score history displays the new test.

---

# 34. Sample Teacher Workflow

1. Teacher opens `/login`.
2. Teacher logs in.
3. Frontend identifies role `teacher` or `admin`.
4. Frontend redirects to Teacher Dashboard.
5. Teacher searches for student number `STU001`.
6. Teacher opens the student.
7. Teacher sees Listening, Reading and Writing summary cards.
8. Teacher sees all three graphs.
9. Teacher opens test history.
10. Teacher expands a test.
11. Teacher reviews mistakes and corrections.
12. Teacher can add or edit a result when needed.

---

# 35. Acceptance Tests

The final build is not complete until all of the following are true.

## Authentication

- [ ] Student can log in.
- [ ] Teacher/Admin can log in.
- [ ] Wrong credentials are rejected.
- [ ] Logout clears authenticated state.
- [ ] Expired/invalid token redirects to login.

## Student isolation

- [ ] Student A cannot read Student B's profile.
- [ ] Student A cannot read Student B's scores.
- [ ] Student A cannot edit Student B's scores.
- [ ] Student A cannot delete Student B's scores.
- [ ] Student A cannot read Student B's mistakes.

## Score entry

- [ ] Listening result can be saved.
- [ ] Reading result can be saved.
- [ ] Writing result can be saved.
- [ ] Band accepts only 0.0–9.0 in 0.5 increments.
- [ ] Test name is required.
- [ ] Invalid raw/total combinations are rejected.
- [ ] Multiple mistakes can be saved with one test.

## Student progress

- [ ] Listening chart appears after Listening records exist.
- [ ] Reading chart appears after Reading records exist.
- [ ] Writing chart appears after Writing records exist.
- [ ] Latest band is correct.
- [ ] Best band is correct.
- [ ] Average band is correct.
- [ ] Total test count is correct.

## Teacher portal

- [ ] Teacher sees student list.
- [ ] Teacher can search students.
- [ ] Teacher can open student detail.
- [ ] Teacher can view progress graphs.
- [ ] Teacher can view mistakes.
- [ ] Teacher can create a result for a student.
- [ ] Teacher can edit/delete according to authorization rules.
- [ ] Teacher can reset password according to authorization rules.

## Deployment

- [ ] Backend can run locally.
- [ ] Frontend can run locally.
- [ ] Full project can run using the supplied startup script.
- [ ] Frontend production build succeeds.
- [ ] Backend tests pass.
- [ ] SPA routes work after refresh in production.
- [ ] Production backend connects to PostgreSQL.
- [ ] Health endpoint returns success.
- [ ] CORS is correctly configured.

---

# 36. Automated Test Scenarios

Backend test suite must cover at least:

1. bootstrap/admin login,
2. student creation,
3. student login,
4. teacher login if teacher creation is implemented,
5. student creates score,
6. student creates multiple mistakes,
7. progress response calculation,
8. student cannot access another student's data,
9. teacher can access student's data,
10. invalid band rejected,
11. invalid raw score rejected,
12. score update,
13. score delete,
14. password change,
15. student password reset by authorized teacher/admin,
16. health endpoint.

Frontend validation should at minimum include:

- TypeScript compile,
- production build,
- route rendering,
- API error handling for 401/403/404/409,
- score form validation.

---

# 37. Performance Targets

For a small training-centre deployment:

- dashboard API should normally respond quickly under ordinary small workloads,
- student search should not require full-page reload,
- chart rendering should remain responsive with hundreds of test records,
- API responses should avoid unnecessarily large payloads.

Do not add complex infrastructure such as Redis, background workers, or microservices for the MVP.

---

# 38. Reliability Requirements

The app must:

- show clear error states when backend is unavailable,
- not lose form data because of a harmless render,
- prevent duplicate form submissions,
- not delete data accidentally without confirmation,
- preserve database records across backend restarts,
- use PostgreSQL for production persistence.

---

# 39. Logging

Backend logs should help diagnose:

- startup problems,
- database connection problems,
- unexpected request failures.

Do not log:

- passwords,
- password reset values,
- JWT tokens,
- sensitive personal information unnecessarily.

Frontend logs should be minimal in production.

---

# 40. README Requirements

The root README must explain, in plain language:

1. What the application does.
2. Project structure.
3. Prerequisites.
4. Windows setup.
5. macOS/Linux setup.
6. One-command startup.
7. How to create the first admin/teacher account.
8. How students are created.
9. How to use the Student Portal.
10. How to use the Teacher Portal.
11. Backend environment variables.
12. Frontend environment variables.
13. Local database behaviour.
14. PostgreSQL production setup.
15. Deployment steps.
16. How to run tests.
17. Common errors and fixes.
18. API documentation URL.
19. How to create a production build.

---

# 41. Common Error Prevention

Codex must explicitly guard against these known failure classes:

### Python dependency issues

Keep `requirements.txt` complete. In particular, avoid importing optional libraries without listing them.

### CORS errors

Read frontend origin(s) from `CORS_ORIGINS` and document the exact deployed frontend URL to place there.

### Database errors

Give a clear error when `DATABASE_URL` is invalid. Do not silently fall back to SQLite in production.

### Frontend API URL errors

Never hard-code `localhost` into production code.

### SPA refresh 404

Configure the static host for SPA fallback.

### Port errors

Backend production command must support hosting platforms that provide a dynamic `PORT`.

### Windows startup errors

Scripts must use Windows-compatible commands and show actionable messages.

### Token state errors

On a 401, clear authentication state and redirect to login.

---

# 42. Deployment Checklist

Before deployment:

```text
[ ] npm install works
[ ] npm run build works
[ ] backend venv works
[ ] pip install -r requirements.txt works
[ ] pytest passes
[ ] frontend points to backend URL
[ ] backend CORS includes frontend URL
[ ] SECRET_KEY changed from example value
[ ] production DATABASE_URL configured
[ ] PostgreSQL schema/migrations applied
[ ] bootstrap admin credentials changed
[ ] health endpoint works
[ ] student login tested
[ ] teacher login tested
[ ] score creation tested
[ ] progress graph tested
[ ] teacher student search tested
```

---

# 43. Final ZIP Requirements for Codex

At the end of implementation, Codex must produce a single ZIP similar to:

```text
IELTS_Student_Progress_FullStack.zip
```

Inside it:

```text
ielts-student-progress/
  backend/
  frontend/
  scripts/
  README.md
  SRS.md
  docker-compose.yml
  render.yaml
  .gitignore
```

Do not include:

- `.venv/`
- `node_modules/`
- database files containing real student data,
- `.env` with real secrets,
- API keys,
- passwords,
- JWT secrets,
- editor cache folders,
- Python `__pycache__` folders.

The ZIP should be source-code deployable, not a ZIP containing the developer's local machine environment.

---

# 44. Definition of Done

The implementation is DONE only when:

1. The supplied backend is successfully converted into a full-stack application.
2. Student Portal works end-to-end.
3. Teacher/Admin Portal works end-to-end.
4. Login works for both roles.
5. Students can store all required IELTS result data.
6. Mistakes are stored per test.
7. Listening/Reading/Writing progress graphs work.
8. Teacher can inspect individual student progress.
9. Authorization is enforced server-side.
10. Local development is documented and tested.
11. Production PostgreSQL configuration is documented.
12. Frontend production build succeeds.
13. Backend automated tests pass.
14. No known syntax/build errors remain.
15. The final ZIP contains the entire project and excludes machine-specific environments and secrets.

---

# 45. Codex Execution Prompt

Use the following section as the direct instruction to Codex.

```text
You are a senior full-stack software engineer.

I have supplied a ZIP containing an existing FastAPI backend for an IELTS Student Progress Portal. Your job is to turn it into a COMPLETE, RUNNABLE, DEPLOYABLE FULL-STACK WEBSITE.

SOURCE OF TRUTH:
- Read the existing backend code before modifying it.
- Read this SRS completely before coding.
- Preserve working backend functionality.
- Treat this SRS as the product specification.

GOAL:
Build a complete IELTS Student Progress Portal with:
1. Student Portal
2. Teacher/Admin Portal
3. React/Vite/TypeScript frontend
4. FastAPI/Python backend
5. PostgreSQL production support
6. SQLite local support
7. JWT authentication
8. Listening, Reading and Writing score tracking
9. Per-test mistake tracking
10. Separate progress graphs for Listening, Reading and Writing
11. Responsive UI
12. Automated tests
13. Windows one-command local startup
14. Production deployment configuration
15. Final source-code ZIP

IMPORTANT:
- Do not fabricate student data.
- Do not fabricate band scores.
- Do not leave unfinished buttons.
- Do not ask me unnecessary clarification questions. Use the SRS assumptions.
- Do not remove working backend features unless necessary.
- If you discover a bug in the existing backend, fix it and add a regression test.
- If the backend API and SRS differ, make them consistent and update the frontend/tests/documentation.

FRONTEND:
Use React + Vite + TypeScript.
Use React Router.
Use Recharts for progress charts.
Keep dependencies minimal.
Create protected routes based on role.
Build a clear Student Dashboard and Teacher Dashboard.

STUDENT FEATURES:
- login
- dashboard
- Listening/Reading/Writing cards
- latest/best/average/test count
- three progress graphs
- add test
- add multiple mistakes in one submission
- test history
- test detail
- edit/delete test
- profile
- change password

TEACHER/ADMIN FEATURES:
- login
- dashboard
- student count
- test count
- searchable student list
- student detail page
- three progress graphs for selected student
- test history
- mistakes
- create test for student
- edit/delete as authorized
- edit student profile
- reset student password
- change own password

DATA RULES:
Skills are ONLY listening, reading, writing.
Band is 0.0 through 9.0 in 0.5 increments.
Test name is required.
Test date is required/stored.
Raw score and total questions are optional.
Raw score cannot exceed total questions.
Mistakes have optional category/question reference/correction and required description.

SECURITY:
Enforce authorization in backend, not just frontend.
Students can access only themselves.
Teachers/Admins can access student records according to role rules.
Never expose password hashes.
Never log passwords or JWTs.
Use environment variables for secrets.
Configure CORS correctly.

DEPLOYMENT:
Frontend must be deployable as a static SPA to Vercel/Netlify or equivalent.
Backend must be deployable as a Docker/Python service to Render or equivalent.
Production database must be PostgreSQL.
Do not depend on persistent SQLite in production.
Support dynamic PORT in the backend.
Provide health check.
Provide frontend SPA fallback configuration.
Provide README deployment steps.

LOCAL DEVELOPMENT:
The repository must include scripts/run.bat, scripts/run.ps1 and scripts/stop.bat.
A new Windows user should be able to understand how to start the project from README.md.

TESTING:
Before declaring completion:
- run Python compile checks
- run pytest
- run frontend type-check/build
- test authentication
- test score creation
- test mistakes
- test progress calculations
- test student isolation
- test teacher access
- test password change/reset
- test health endpoint

FINAL OUTPUT:
Create a clean root project.
Do not include .venv, node_modules, __pycache__, real database files, .env, secrets, API keys or passwords.
Include SRS.md and README.md.
Create the final source ZIP:
IELTS_Student_Progress_FullStack.zip

Before finishing, give a concise report containing:
- files created/changed,
- commands used to validate the project,
- test results,
- exact local startup commands,
- exact deployment steps,
- required environment variables,
- any remaining known limitation.

Do not claim a test passed unless you actually ran it.
```

---

# 46. Recommended Build Order for Codex

Use this implementation order to reduce integration errors:

1. Inspect current backend.
2. Run existing backend tests.
3. Fix backend defects found by tests.
4. Add any missing backend endpoints required by this SRS.
5. Add/verify database migrations.
6. Build frontend project shell.
7. Implement authentication context and protected routing.
8. Implement Student Portal.
9. Implement score/mistake forms.
10. Implement progress charts.
11. Implement Teacher/Admin Portal.
12. Connect every page to real backend endpoints.
13. Add loading/error/empty states.
14. Add responsive design.
15. Add frontend production configuration.
16. Add Windows startup scripts.
17. Run the full validation suite.
18. Clean secrets/cache/developer-only folders.
19. Build final ZIP.
20. Produce final run/deployment README.

---

# 47. Explicit Scope Boundary

MVP includes:

- Students,
- Teachers/Admins,
- Listening,
- Reading,
- Writing,
- test names,
- dates,
- band scores,
- optional raw scores,
- mistakes,
- corrections,
- progress charts,
- teacher monitoring,
- password management.

MVP does NOT require:

- IELTS Speaking tracking,
- official IELTS score calculation,
- payment system,
- subscriptions,
- video lessons,
- messaging/chat,
- email marketing,
- AI grading,
- automated essay scoring,
- mobile apps,
- social features,
- public student profiles.

These can be future phases.

---

# 48. Future Enhancements (Not Required Now)

Possible future versions may add:

- Speaking score tracking,
- Overall band calculation,
- target band and target date,
- weekly/monthly reports,
- teacher comments by mistake,
- mistake analytics by category,
- CSV import/export,
- student bulk import,
- printable progress reports,
- email notifications,
- teacher-created assignments,
- multiple teachers/classes,
- organization-level admin,
- audit log,
- password reset by email,
- two-factor authentication.

Do not implement these future features unless required for a correctness/security issue.

---

# 49. Final Instruction

The desired outcome is not a prototype screenshot and not backend-only API code.

The desired outcome is a **single clean full-stack project** that a developer can open, install, run locally, configure with environment variables, deploy, and hand to students and teachers.

The current backend ZIP is the starting point. Codex must finish the missing frontend and portal functionality and verify the entire application end-to-end.
