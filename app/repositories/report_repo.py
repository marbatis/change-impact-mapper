from __future__ import annotations

import json
from typing import Any, Optional

from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.models import ImpactReportRecord


class ReportRepository:
    def __init__(self, db: Session):
        self.db = db

    def save(self, report: dict[str, Any]) -> None:
        rec = ImpactReportRecord(
            report_id=report["report_id"],
            change_id=report["change_id"],
            target_node=report["target_node"],
            report_json=json.dumps(report, default=str),
        )
        self.db.add(rec)
        self.db.commit()

    def get(self, report_id: str) -> Optional[dict[str, Any]]:
        rec = self.db.scalar(select(ImpactReportRecord).where(ImpactReportRecord.report_id == report_id))
        if not rec:
            return None
        return json.loads(rec.report_json)

    def list_recent(self, limit: int = 50) -> list[dict[str, Any]]:
        rows = self.db.scalars(
            select(ImpactReportRecord).order_by(desc(ImpactReportRecord.created_at)).limit(limit)
        ).all()
        return [json.loads(row.report_json) for row in rows]
