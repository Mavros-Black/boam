from datetime import date

from app.models import Job, JobStatus, Application
from app.repositories.jobs import create_job, get_job, update_job_status
from app.repositories.applications import create_application, get_application, update_application_success


def test_create_and_get_job(db_session):
    job = Job(
        source="indeed",
        listing_id="abc-123",
        title="Frontend Engineer",
        company="Acme",
        location="Remote",
        remote=True,
        url="https://example.com/job/1",
        date_posted=date.today(),
        description="Build UIs",
        skills=["react", "typescript"],
        tech_stack=["react", "node"],
        match_score=87.5,
    )
    created = create_job(db_session, job)

    assert created.id is not None

    fetched = get_job(db_session, created.id)
    assert fetched is not None
    assert fetched.title == "Frontend Engineer"
    assert fetched.status == JobStatus.NEW


def test_update_job_status(db_session):
    job = Job(
        source="indeed",
        title="Backend Engineer",
        company="Acme",
        location="Remote",
        remote=True,
        url="https://example.com/job/2",
    )
    created = create_job(db_session, job)
    updated = update_job_status(db_session, created.id, JobStatus.APPLIED)

    assert updated is not None
    assert updated.status == JobStatus.APPLIED


def test_create_and_update_application(db_session):
    job = Job(
        source="indeed",
        title="Data Engineer",
        company="Acme",
        location="Remote",
        remote=True,
        url="https://example.com/job/3",
    )
    job = create_job(db_session, job)

    app = Application(job_id=job.id, notes="Submitted via portal", success=False)
    app = create_application(db_session, app)

    fetched = get_application(db_session, app.id)
    assert fetched is not None
    assert fetched.success is False

    updated = update_application_success(db_session, app.id, True)
    assert updated is not None
    assert updated.success is True