from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional
from uuid import uuid4

from sqlalchemy.orm import Session

from app.repositories.report_repo import ReportRepository
from app.schemas.models import ChangeRequest, HistoryItem, ImpactReport
from app.services.graph_loader import GraphLoader
from app.services.impact_engine import ImpactEngine
from app.services.recommendation_engine import RecommendationEngine
from app.services.reporting import build_report_memo
from app.services.risk_scoring import RiskScoring


class ImpactService:
    def __init__(self, db: Session):
        self.repo = ReportRepository(db)
        self.graph = GraphLoader().load()
        self.engine = ImpactEngine()
        self.scoring = RiskScoring()
        self.reco = RecommendationEngine()
        root = Path(__file__).resolve().parents[2]
        self.sample_dir = root / "data" / "samples"

    def run_change(self, change: ChangeRequest) -> ImpactReport:
        impacted = self.engine.impacted_nodes(self.graph, change.target_node)
        paths = self.engine.critical_paths(self.graph, change.target_node)
        risky = self.scoring.risky_consumers(self.graph, impacted)
        tests = self.reco.recommended_tests(self.graph, risky, change.change_type)
        approvals = self.reco.required_approvals(self.graph, risky, change.risk_level)

        report = ImpactReport(
            report_id=str(uuid4()),
            change_id=change.change_id,
            target_node=change.target_node,
            impacted_nodes=impacted,
            critical_paths=paths,
            risky_consumers=risky,
            recommended_tests=tests,
            required_approvals=approvals,
            report_memo=build_report_memo(change.change_id, change.target_node, len(impacted), len(risky), approvals),
            graph_points=self.scoring.graph_points(self.graph, impacted),
            created_at=datetime.now(timezone.utc),
        )
        self.repo.save(report.model_dump(mode="json"))
        return report

    def run_sample(self, sample_id: str) -> ImpactReport:
        path = self.sample_dir / f"{sample_id}.json"
        if not path.exists():
            raise FileNotFoundError(sample_id)
        payload = json.loads(path.read_text(encoding="utf-8"))
        return self.run_change(ChangeRequest.model_validate(payload))

    def get_report(self, report_id: str) -> Optional[ImpactReport]:
        raw = self.repo.get(report_id)
        if not raw:
            return None
        return ImpactReport.model_validate(raw)

    def history(self, limit: int = 50) -> list[HistoryItem]:
        rows = self.repo.list_recent(limit=limit)
        return [
            HistoryItem(
                report_id=row["report_id"],
                change_id=row["change_id"],
                target_node=row["target_node"],
                created_at=row["created_at"],
            )
            for row in rows
        ]

    def sample_ids(self) -> list[str]:
        return sorted(path.stem for path in self.sample_dir.glob("*.json"))
