from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

import networkx as nx


class GraphLoader:
    def __init__(self, graph_path: Optional[Path] = None):
        root = Path(__file__).resolve().parents[2]
        self.graph_path = graph_path or (root / "data" / "graph" / "estate_graph.json")

    def load(self) -> nx.DiGraph:
        payload = json.loads(self.graph_path.read_text(encoding="utf-8"))
        graph = nx.DiGraph()
        for node in payload["nodes"]:
            graph.add_node(node["id"], **node)
        for edge in payload["edges"]:
            graph.add_edge(edge["from"], edge["to"], relation=edge.get("relation", "depends_on"))
        return graph
