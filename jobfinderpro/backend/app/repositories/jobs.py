from __future__ import annotations
from typing import Optional, Sequence, Tuple
from sqlalchemy import select, and_
from sqlalchemy.orm import Session
from app.models import Job, JobStatus
from app.scrapers.base import JobDraft


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


def _find_existing(session: Session, draft: JobDraft) -> Optional[Job]:
    if draft.listing_id:
        stmt = select(Job).where(and_(Job.source == draft.source, Job.listing_id == draft.listing_id))
        job = session.execute(stmt).scalars().first()
        if job:
            return job
    stmt = select(Job).where(and_(Job.source == draft.source, Job.url == str(draft.url)))
    return session.execute(stmt).scalars().first()


def upsert_job_from_draft(session: Session, draft: JobDraft, *, match_score: float) -> Tuple[bool, bool]:
    existing = _find_existing(session, draft)
    if existing:
        updated = False
        fields = {
            "title": draft.title,
            "company": draft.company,
            "location": draft.location,
            "remote": bool(draft.remote) if draft.remote is not None else existing.remote,
            "url": str(draft.url),
            "date_posted": draft.date_posted,
            "description": draft.description,
            "skills": draft.skills,
            "tech_stack": draft.tech_stack,
            "match_score": match_score,
        }
        for k, v in fields.items():
            if getattr(existing, k) != v and v is not None:
                setattr(existing, k, v)
                updated = True
        if updated:
            session.commit()
        return False, updated

    job = Job(
        source=draft.source,
        listing_id=draft.listing_id,
        title=draft.title,
        company=draft.company,
        location=draft.location,
        remote=bool(draft.remote) if draft.remote is not None else False,
        url=str(draft.url),
        date_posted=draft.date_posted,
        description=draft.description,
        skills=draft.skills,
        tech_stack=draft.tech_stack,
        match_score=match_score,
    )
    session.add(job)
    session.commit()
    return True, False