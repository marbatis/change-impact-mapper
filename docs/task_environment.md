# Task Environment

## 1. Rational objective
Map blast radius for a synthetic change request using deterministic graph analysis.

## 2. PEAS
- Performance: correct impact traversal, actionable test recommendations, explicit approvals.
- Environment: synthetic hybrid estate graph and change requests.
- Actuators: API responses, web report pages.
- Sensors: target node, change type, risk level, graph topology.

## 3. Environmental dimensions
Partially observable and dynamic dependency graph with multi-hop risk propagation.

## 4. Problem formalization
Given change request c and directed graph G, compute impacted descendants, critical paths, risky consumers, and required safeguards.

## 5. Architecture choice
Graph loader + impact engine + deterministic scoring and recommendation modules.

## 6. Guardrails / workflow maturity
No production actions, deterministic outputs, transparent approval/test logic.
