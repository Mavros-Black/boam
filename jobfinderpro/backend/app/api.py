from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException, Query, Response
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy.orm import Session
import csv
import io

from app.db import SessionLocal
from app.services.scrape import run_scrape
from app.scrapers.base import Scraper
from app.schemas import JobOut, JobStatusUpdate, ApplyResponse
from app.models import Job, JobStatus
from app.repositories.jobs import list_jobs_filtered, get_job, update_job_status

router = APIRouter(prefix="/api")


class ScrapeCriteria(BaseModel):
    keywords: str
    location: Optional[str] = None
    remote: Optional[bool] = None


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/scrape")
def scrape(criteria: ScrapeCriteria, db: Session = Depends(get_db)):
    summary = run_scrape(db, scrapers=[], keywords=criteria.keywords, location=criteria.location, remote=criteria.remote)
    return {"task_id": None, "found": summary["inserted"]}


@router.get("/jobs", response_model=List[JobOut])
def list_jobs_api(
    db: Session = Depends(get_db),
    status: Optional[str] = Query(None),
    location: Optional[str] = Query(None),
    min_match: Optional[float] = Query(None),
    q: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
):
    jobs = list_jobs_filtered(db, status=status, location=location, min_match=min_match, q=q, page=page, page_size=page_size)
    return jobs


@router.get("/jobs/{job_id}", response_model=JobOut)
def get_job_api(job_id: int, db: Session = Depends(get_db)):
    job = get_job(db, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@router.put("/jobs/{job_id}/status", response_model=JobOut)
def update_job_status_api(job_id: int, body: JobStatusUpdate, db: Session = Depends(get_db)):
    try:
        new_status = JobStatus(body.status)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid status")
    job = update_job_status(db, job_id, new_status)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@router.post("/apply/{job_id}", response_model=ApplyResponse)
def apply_job_api(job_id: int, db: Session = Depends(get_db)):
    # Phase 6 will implement automation. For now, simulate success and set status.
    job = update_job_status(db, job_id, JobStatus.APPLIED)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return ApplyResponse(success=True, status=job.status.value)


@router.get("/export.csv")
def export_csv_api(
    db: Session = Depends(get_db),
    status: Optional[str] = Query(None),
    location: Optional[str] = Query(None),
    min_match: Optional[float] = Query(None),
    q: Optional[str] = Query(None),
):
    jobs = list_jobs_filtered(db, status=status, location=location, min_match=min_match, q=q, page=1, page_size=1000)
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(["id", "title", "company", "location", "match_score", "status", "url"])
    for j in jobs:
        writer.writerow([j.id, j.title, j.company, j.location, j.match_score, j.status, j.url])
    csv_data = buf.getvalue()
    return Response(content=csv_data, media_type="text/csv")