"""Pytest smoke + integration tests for the backend (uses fallback router)."""
import os

os.environ["DATABASE_URL"] = "sqlite:///./test_campus.db"
os.environ["GEMINI_API_KEY"] = ""  # force deterministic fallback in tests

from fastapi.testclient import TestClient  # noqa: E402

from app.database import Base, engine  # noqa: E402
from app.main import app  # noqa: E402
from app.seed import seed  # noqa: E402

Base.metadata.create_all(bind=engine)
seed()
client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "healthy"


def test_login_and_me():
    r = client.post("/api/v1/auth/login", json={"email": "student@campus.edu", "password": "student123"})
    assert r.status_code == 200
    token = r.json()["access_token"]
    me = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me.status_code == 200
    assert me.json()["email"] == "student@campus.edu"


def test_library_listing():
    r = client.get("/api/v1/library/books")
    assert r.status_code == 200
    assert len(r.json()) >= 1


def test_agent_routes_to_library():
    r = client.post("/api/v1/chat", json={"message": "Is the DBMS book available?"})
    assert r.status_code == 200
    assert r.json()["tool_used"] == "search_library"


def test_agent_routes_to_cafeteria():
    r = client.post("/api/v1/chat", json={"message": "What is today's lunch?"})
    assert r.status_code == 200
    assert r.json()["tool_used"] == "search_menu"


def test_agent_routes_to_events():
    r = client.post("/api/v1/chat", json={"message": "When is the hackathon?"})
    assert r.status_code == 200
    assert r.json()["tool_used"] == "search_events"


def test_agent_routes_to_academics():
    r = client.post("/api/v1/chat", json={"message": "What is the attendance requirement?"})
    assert r.status_code == 200
    assert r.json()["tool_used"] == "search_academics"


def test_dbms_book_found_in_fallback():
    # full natural-language question must still find the seeded DBMS book
    r = client.post("/api/v1/chat", json={"message": "Is the DBMS book available?"})
    assert r.status_code == 200
    assert "Database System Concepts" in r.json()["answer"]


def test_hackathon_event_found_in_fallback():
    r = client.post("/api/v1/chat", json={"message": "When is the hackathon?"})
    assert r.status_code == 200
    assert "Hackathon" in r.json()["answer"]


def test_admin_required_for_create_book():
    # no token -> 401
    r = client.post("/api/v1/library/books", json={"title": "X"})
    assert r.status_code == 401
