from __future__ import annotations

from datetime import datetime
from typing import List

from pydantic import BaseModel


class ChangeRequest(BaseModel):
    change_id: str
    target_node: str
    change_type: str
    rollout_window: str
    risk_level: str
    notes: str = ""


class ImpactReport(BaseModel):
    report_id: str
    change_id: str
    target_node: str
    impacted_nodes: List[str]
    critical_paths: List[List[str]]
    risky_consumers: List[str]
    recommended_tests: List[str]
    required_approvals: List[str]
    report_memo: str
    graph_points: list[dict]
    created_at: datetime


class HistoryItem(BaseModel):
    report_id: str
    change_id: str
    target_node: str
    created_at: datetime
