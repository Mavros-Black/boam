from __future__ import annotations
from typing import Iterable, Protocol, Optional
from datetime import date
from pydantic import BaseModel, HttpUrl


class JobDraft(BaseModel):
    source: str
    listing_id: Optional[str] = None
    title: str
    company: Optional[str] = None
    location: Optional[str] = None
    remote: Optional[bool] = None
    url: HttpUrl
    date_posted: Optional[date] = None
    description: Optional[str] = None
    skills: Optional[list[str]] = None
    tech_stack: Optional[list[str]] = None


class Scraper(Protocol):
    def search(self, *, keywords: str, location: Optional[str] = None, remote: Optional[bool] = None) -> Iterable[JobDraft]:
        ...