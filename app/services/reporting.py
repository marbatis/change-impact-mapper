from __future__ import annotations


def build_report_memo(
    change_id: str,
    target_node: str,
    impacted_count: int,
    risky_count: int,
    approvals: list[str],
) -> str:
    approval_text = ", ".join(approvals)
    return (
        f"Change {change_id} targeting {target_node} impacts {impacted_count} nodes with "
        f"{risky_count} high-risk consumers. Required approvals: {approval_text}."
    )
