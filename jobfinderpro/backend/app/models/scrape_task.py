from __future__ import annotations
from datetime import datetime
from typing import Optional
from sqlalchemy import Integer, DateTime, String, Boolean, JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class ScrapeTask(Base):
    __tablename__ = "scrape_tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    query: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    location: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    remote: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="NEW", nullable=False)
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    finished_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    stats: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)