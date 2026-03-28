from __future__ import annotations


def test_sample_route_returns_report(client) -> None:
    response = client.post("/api/impact/sample/auth_schema_change")
    assert response.status_code == 201
    body = response.json()
    assert body["change_id"] == "CHG-9001"
    assert body["impacted_nodes"]


def test_upload_route_works(client) -> None:
    payload = {
        "change_id": "CHG-UP-1",
        "target_node": "payments-queue",
        "change_type": "dependency update",
        "rollout_window": "2026-04-10T01:00:00Z",
        "risk_level": "medium",
        "notes": "test upload"
    }
    import json

    response = client.post(
        "/api/impact/upload",
        files={"file": ("change.json", json.dumps(payload), "application/json")},
    )
    assert response.status_code == 201
    assert response.json()["change_id"] == "CHG-UP-1"


def test_web_history_renders(client) -> None:
    client.post("/api/impact/sample/payments_queue_update")
    response = client.get("/history")
    assert response.status_code == 200
    assert "History" in response.text
