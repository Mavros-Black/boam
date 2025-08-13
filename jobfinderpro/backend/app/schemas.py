from __future__ import annotations
from typing import Optional, List
from datetime import datetime, date
from pydantic import BaseModel, HttpUrl, Field


class JobOut(BaseModel):
    id: int
    source: str
    listing_id: Optional[str] = None
    title: str
    company: Optional[str] = None
    location: Optional[str] = None
    remote: bool = False
    url: HttpUrl
    date_posted: Optional[date] = None
    description: Optional[str] = None
    skills: Optional[List[str]] = None
    tech_stack: Optional[List[str]] = None
    match_score: Optional[float] = None
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }


class JobStatusUpdate(BaseModel):
    status: str = Field(pattern=r"^(NEW|APPLIED|SKIPPED)$")


class ApplyResponse(BaseModel):
    success: bool
    status: str