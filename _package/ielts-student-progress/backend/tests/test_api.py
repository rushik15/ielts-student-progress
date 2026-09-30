import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
TEST_DB = Path(__file__).parent / "test_progress.db"
os.environ["DATABASE_URL"] = f"sqlite:///{TEST_DB.as_posix()}"
os.environ["SECRET_KEY"] = "test-secret-with-at-least-32-characters"
os.environ["BOOTSTRAP_ADMIN_PASSWORD"] = "admin-pass"

from fastapi.testclient import TestClient
from app.main import app


def auth(client, number, password):
    response = client.post("/api/v1/auth/login", json={"student_number": number, "password": password})
    assert response.status_code == 200
    return {"Authorization": f"Bearer {response.json()['access_token']}"}


def test_full_student_teacher_flow():
    if TEST_DB.exists(): TEST_DB.unlink()
    with TestClient(app) as client:
        assert client.get("/api/v1/health").json() == {"status": "ok"}
        admin = auth(client, "admin001", "admin-pass")
        student = client.post("/api/v1/students", headers=admin, json={"student_number": "STU001", "full_name": "Asha Student", "password": "student-pass"})
        assert student.status_code == 201
        second = client.post("/api/v1/students", headers=admin, json={"student_number": "STU002", "full_name": "Other Student", "password": "student-pass"})
        assert second.status_code == 201
        student_headers = auth(client, "STU001", "student-pass")
        invalid = client.post("/api/v1/scores", headers=student_headers, json={"skill": "listening", "test_name": "Bad", "test_date": "2026-09-01", "band_score": 6.2})
        assert invalid.status_code == 422
        score = client.post("/api/v1/scores", headers=student_headers, json={"skill": "listening", "test_name": "Cambridge 19", "test_date": "2026-09-01", "band_score": 6.5, "raw_score": 30, "total_questions": 40, "mistakes": [{"description": "Spelling"}, {"category": "distractor", "description": "Changed answer"}]})
        assert score.status_code == 201
        score_id = score.json()["id"]
        assert len(score.json()["mistakes"]) == 2
        progress = client.get("/api/v1/progress/listening", headers=student_headers).json()
        assert progress["latest"] == 6.5 and progress["count"] == 1
        assert client.get(f"/api/v1/students/{second.json()['id']}", headers=student_headers).status_code == 403
        assert client.patch(f"/api/v1/scores/{score_id}", headers=student_headers, json={"band_score": 7.0}).status_code == 200
        assert client.post("/api/v1/auth/change-password", headers=student_headers, json={"current_password": "student-pass", "new_password": "new-pass"}).status_code == 204
        assert auth(client, "STU001", "new-pass")
        assert client.get("/api/v1/students?search=ASHA", headers=admin).status_code == 200
        assert client.get(f"/api/v1/students/{student.json()['id']}/progress/listening", headers=admin).status_code == 200
        assert client.post(f"/api/v1/students/{student.json()['id']}/password", headers=admin, json={"new_password": "reset-pass"}).status_code == 204
        assert auth(client, "STU001", "reset-pass")
        assert client.delete(f"/api/v1/scores/{score_id}", headers=admin).status_code == 204
