from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import DateTime, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class ImpactReportRecord(Base):
    __tablename__ = "impact_reports"

    report_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    change_id: Mapped[str] = mapped_column(String(128), index=True)
    target_node: Mapped[str] = mapped_column(String(128), index=True)
    report_json: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
