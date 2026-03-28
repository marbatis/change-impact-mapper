from __future__ import annotations

import networkx as nx


class RecommendationEngine:
    def recommended_tests(self, graph: nx.DiGraph, risky_consumers: list[str], change_type: str) -> list[str]:
        tests = [
            "Run contract tests on direct consumers",
            "Run integration tests on risky downstream paths",
        ]
        if "schema" in change_type.lower():
            tests.append("Execute backward-compatibility schema checks")
        if any(graph.nodes[n].get("type") == "database" for n in risky_consumers if n in graph.nodes):
            tests.append("Run read/write regression tests against primary database paths")
        return tests[:5]

    def required_approvals(self, graph: nx.DiGraph, risky_consumers: list[str], risk_level: str) -> list[str]:
        approvals = ["service_owner"]
        if risk_level.lower() in {"high", "critical"}:
            approvals.append("platform_ops")
        if any(graph.nodes[n].get("type") == "identity" for n in risky_consumers if n in graph.nodes):
            approvals.append("security_review")
        return sorted(set(approvals))
