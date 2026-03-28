from __future__ import annotations

from app.services.graph_loader import GraphLoader
from app.services.impact_engine import ImpactEngine
from app.services.recommendation_engine import RecommendationEngine
from app.services.risk_scoring import RiskScoring


def test_graph_traversal_finds_descendants() -> None:
    graph = GraphLoader().load()
    impacted = ImpactEngine().impacted_nodes(graph, "auth-service")
    assert "auth-service" in impacted
    assert "api-gateway" in impacted
    assert "mobile-app" in impacted


def test_risk_scoring_flags_critical_nodes() -> None:
    graph = GraphLoader().load()
    impacted = ImpactEngine().impacted_nodes(graph, "payments-service")
    risky = RiskScoring().risky_consumers(graph, impacted)
    assert "payments-service" in risky


def test_recommendations_include_schema_check() -> None:
    graph = GraphLoader().load()
    risky = ["auth-service", "api-gateway"]
    tests = RecommendationEngine().recommended_tests(graph, risky, "schema change")
    assert any("schema" in t.lower() for t in tests)
