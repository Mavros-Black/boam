from __future__ import annotations
from typing import Optional, Sequence
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models import Job, JobStatus


def create_job(session: Session, job: Job) -> Job:
    session.add(job)
    session.commit()
    session.refresh(job)
    return job


def get_job(session: Session, job_id: int) -> Optional[Job]:
    return session.get(Job, job_id)


def update_job_status(session: Session, job_id: int, status: JobStatus) -> Optional[Job]:
    job = session.get(Job, job_id)
    if not job:
        return None
    job.status = status
    session.commit()
    session.refresh(job)
    return job


def list_jobs(session: Session, limit: int = 100) -> Sequence[Job]:
    stmt = select(Job).limit(limit)
    return list(session.execute(stmt).scalars().all())