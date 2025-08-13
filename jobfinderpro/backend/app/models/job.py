from __future__ import annotations
from datetime import datetime, date
from enum import Enum
from typing import List, Optional
from sqlalchemy import String, Integer, DateTime, Date, Boolean, Text, Enum as SAEnum, Float
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import JSON

from app.db import Base


class JobStatus(str, Enum):
    NEW = "NEW"
    APPLIED = "APPLIED"
    SKIPPED = "SKIPPED"


class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    source: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    listing_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    company: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)
    location: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)
    remote: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    url: Mapped[str] = mapped_column(String(1024), nullable=False)
    date_posted: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Use JSONB if available, fallback to JSON
    skills: Mapped[Optional[list]] = mapped_column(
        JSONB().with_variant(JSON, "sqlite"), nullable=True
    )
    tech_stack: Mapped[Optional[list]] = mapped_column(
        JSONB().with_variant(JSON, "sqlite"), nullable=True
    )

    match_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    status: Mapped[JobStatus] = mapped_column(SAEnum(JobStatus), default=JobStatus.NEW, nullable=False, index=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)