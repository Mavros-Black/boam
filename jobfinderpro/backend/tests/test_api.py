from __future__ import annotations
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.api import get_db
from app.models import Job


client = TestClient(app)


def seed_job(session: Session) -> Job:
    job = Job(
        source="seed",
        listing_id="x1",
        title="Seeded Job",
        company="Acme",
        location="Remote",
        remote=True,
        url="https://example.com/seed",
        description="Python FastAPI",
        match_score=80.0,
    )
    session.add(job)
    session.commit()
    session.refresh(job)
    return job


def test_jobs_endpoints(db_session):
    # Override dependency to use test session
    app.dependency_overrides[get_db] = lambda: db_session

    j = seed_job(db_session)

    # List
    r = client.get("/api/jobs")
    assert r.status_code == 200
    assert isinstance(r.json(), list)

    # Get detail
    r = client.get(f"/api/jobs/{j.id}")
    assert r.status_code == 200
    data = r.json()
    assert data["title"] == "Seeded Job"

    # Update status
    r = client.put(f"/api/jobs/{j.id}/status", json={"status": "SKIPPED"})
    assert r.status_code == 200
    assert r.json()["status"] == "SKIPPED"

    # Apply (stub)
    r = client.post(f"/api/apply/{j.id}")
    assert r.status_code == 200
    assert r.json()["success"] is True

    # Export CSV
    r = client.get("/api/export.csv")
    assert r.status_code == 200
    assert r.headers["content-type"].startswith("text/csv")