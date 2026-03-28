from __future__ import annotations

from typing import List

import networkx as nx


class ImpactEngine:
    def impacted_nodes(self, graph: nx.DiGraph, target_node: str) -> list[str]:
        descendants = nx.descendants(graph, target_node)
        return [target_node] + sorted(descendants)

    def critical_paths(self, graph: nx.DiGraph, target_node: str, max_paths: int = 8) -> List[List[str]]:
        sinks = [node for node in graph.nodes if graph.out_degree(node) == 0]
        all_paths: list[list[str]] = []
        for sink in sinks:
            if sink == target_node:
                continue
            if nx.has_path(graph, target_node, sink):
                for path in nx.all_simple_paths(graph, source=target_node, target=sink, cutoff=6):
                    all_paths.append(path)
                    if len(all_paths) >= max_paths:
                        return all_paths
        return all_paths
