from __future__ import annotations
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.services.scrape import run_scrape
from app.scrapers.base import Scraper

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
    # For now, we will plug in an empty scrapers list; tests will inject fakes
    summary = run_scrape(db, scrapers=[], keywords=criteria.keywords, location=criteria.location, remote=criteria.remote)
    return {"task_id": None, "found": summary["inserted"]}