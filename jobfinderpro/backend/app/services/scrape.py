from __future__ import annotations
from typing import Iterable, List, Dict, Tuple, Optional
from sqlalchemy.orm import Session

from app.scrapers.base import JobDraft, Scraper
from app.repositories.jobs import upsert_job_from_draft
from app.services.match import compute_match_score


def _dedup_key(draft: JobDraft) -> Tuple[str, str]:
    return (draft.source.lower(), (draft.listing_id or str(draft.url)).lower())


def run_scrape(session: Session, *, scrapers: Iterable[Scraper], keywords: str, location: Optional[str] = None, remote: Optional[bool] = None) -> Dict[str, int]:
    seen: set[Tuple[str, str]] = set()
    counts: Dict[str, int] = {"total": 0, "inserted": 0, "updated": 0, "deduped": 0}

    for scraper in scrapers:
        for draft in scraper.search(keywords=keywords, location=location, remote=remote):
            counts["total"] += 1
            key = _dedup_key(draft)
            if key in seen:
                counts["deduped"] += 1
                continue
            seen.add(key)

            # Compute match score
            _, tfidf_component, overlap_component = compute_match_score(
                resume_keywords=keywords.split(),
                job_text=draft.description or ""
            )
            # Use combined score (first element) instead of components
            combined, _, _ = compute_match_score(resume_keywords=keywords.split(), job_text=draft.description or "")

            created, updated = upsert_job_from_draft(session, draft, match_score=combined)
            if created:
                counts["inserted"] += 1
            elif updated:
                counts["updated"] += 1

    return counts