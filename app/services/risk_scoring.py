from __future__ import annotations

import networkx as nx


class RiskScoring:
    NODE_WEIGHTS = {
        "service": 12,
        "database": 18,
        "batch_job": 8,
        "event_stream": 10,
        "external_dependency": 20,
        "identity": 14,
        "observability": 7,
        "notification": 9,
    }

    def risky_consumers(self, graph: nx.DiGraph, impacted_nodes: list[str]) -> list[str]:
        risky: list[tuple[str, int]] = []
        for node in impacted_nodes:
            node_type = graph.nodes[node].get("type", "service")
            criticality = int(graph.nodes[node].get("criticality", 1))
            weight = self.NODE_WEIGHTS.get(node_type, 10)
            score = weight * criticality
            if score >= 30:
                risky.append((node, score))
        risky.sort(key=lambda x: x[1], reverse=True)
        return [name for name, _ in risky]

    def graph_points(self, graph: nx.DiGraph, impacted_nodes: list[str]) -> list[dict]:
        return [
            {
                "id": node,
                "label": node,
                "type": graph.nodes[node].get("type", "service"),
                "criticality": int(graph.nodes[node].get("criticality", 1)),
            }
            for node in impacted_nodes
        ]
