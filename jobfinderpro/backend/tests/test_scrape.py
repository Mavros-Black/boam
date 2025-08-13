from __future__ import annotations
from typing import Iterable, Optional
from datetime import date
from pydantic import AnyUrl

from app.scrapers.base import JobDraft, Scraper
from app.services.scrape import run_scrape
from app.db import SessionLocal


class FakeScraper(Scraper):
    def __init__(self, source: str, drafts: list[JobDraft]):
        self._source = source
        self._drafts = drafts

    def search(self, *, keywords: str, location: Optional[str] = None, remote: Optional[bool] = None) -> Iterable[JobDraft]:
        return self._drafts


def make_draft(source: str, listing_id: str, title: str, url: str, desc: str) -> JobDraft:
    return JobDraft(
        source=source,
        listing_id=listing_id,
        title=title,
        url=url,  # type: ignore[arg-type]
        description=desc,
        date_posted=date.today(),
    )


def test_run_scrape_with_multiple_sources(db_session):
    # Indeed provides two entries, ZipRecruiter one overlapping by URL, Jobright a unique one
    indeed = FakeScraper("indeed", [
        make_draft("indeed", "inc-1", "Python Engineer", "https://indeed.com/j/inc-1", "Python FastAPI SQLAlchemy Postgres"),
        make_draft("indeed", "inc-2", "Frontend Dev", "https://indeed.com/j/inc-2", "React TypeScript Vite"),
    ])
    ziprecruiter = FakeScraper("ziprecruiter", [
        make_draft("ziprecruiter", "zip-1", "Python Engineer", "https://indeed.com/j/inc-1", "Python FastAPI SQLAlchemy Postgres"),  # dedup by url+source differs so not deduped
    ])
    jobright = FakeScraper("jobright", [
        make_draft("jobright", "jr-1", "DevOps Engineer", "https://jobright.ai/j/jr-1", "Docker AWS Kubernetes"),
    ])

    summary = run_scrape(db_session, scrapers=[indeed, ziprecruiter, jobright], keywords="python fastapi sqlalchemy postgres react typescript docker aws")

    # Ensure counts match and no duplicates within same source
    assert summary["total"] == 4
    # No internal dedupe because all keys are unique by (source, listing/url)
    assert summary["deduped"] == 0
    assert summary["inserted"] == 4

    # A second run should update, not insert
    summary2 = run_scrape(db_session, scrapers=[indeed, ziprecruiter, jobright], keywords="python fastapi sqlalchemy postgres react typescript docker aws")
    assert summary2["inserted"] == 0
    assert summary2["updated"] >= 0