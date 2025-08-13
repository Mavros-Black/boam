from __future__ import annotations
from typing import Optional, Sequence
from sqlalchemy import select, or_
from sqlalchemy.orm import Session
from app.models import Job


def list_jobs_filtered(
    session: Session,
    *,
    status: Optional[str] = None,
    location: Optional[str] = None,
    min_match: Optional[float] = None,
    q: Optional[str] = None,
    page: int = 1,
    page_size: int = 20,
) -> Sequence[Job]:
    stmt = select(Job)
    if status:
        stmt = stmt.where(Job.status == status)
    if location:
        stmt = stmt.where(Job.location.ilike(f"%{location}%"))
    if min_match is not None:
        stmt = stmt.where(Job.match_score >= float(min_match))
    if q:
        like = f"%{q}%"
        stmt = stmt.where(or_(Job.title.ilike(like), Job.company.ilike(like), Job.location.ilike(like)))

    stmt = stmt.order_by(Job.match_score.desc().nullslast(), Job.created_at.desc()).offset((page - 1) * page_size).limit(page_size)
    return list(session.execute(stmt).scalars().all())