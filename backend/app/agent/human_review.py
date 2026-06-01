from __future__ import annotations

from app.models import HumanReviewTask, ImpactAnalysis, RiskAssessment, TestCase


def plan_human_review(impact: ImpactAnalysis, risk: RiskAssessment, test_cases: list[TestCase]) -> list[HumanReviewTask]:
    tasks: list[HumanReviewTask] = []
    high_risk = risk.overallRisk in {"high", "critical"} or any(test.priority == "P0" for test in test_cases)
    module_names = {module.name for module in impact.affectedModules}

    if high_risk:
        tasks.append(
            HumanReviewTask(
                id="HR-001",
                title="QA Lead approval for high-risk test plan",
                assigneeRole="QA Lead",
                reason="The generated plan contains high-risk modules or P0/P1 test cases that need human validation.",
            )
        )

    if {"Payment Gateway", "Checkout", "Order Management"} & module_names:
        tasks.append(
            HumanReviewTask(
                id=f"HR-{len(tasks) + 1:03d}",
                title="Release Manager review for revenue-critical workflow",
                assigneeRole="Release Manager",
                reason="Checkout, payment, or order state changes can affect revenue and customer recovery paths.",
            )
        )

    if {"Authentication", "Authorization"} & module_names:
        tasks.append(
            HumanReviewTask(
                id=f"HR-{len(tasks) + 1:03d}",
                title="Security reviewer approval for access-control change",
                assigneeRole="Security Reviewer",
                reason="Authentication and authorization changes require explicit security review.",
            )
        )

    if not tasks:
        tasks.append(
            HumanReviewTask(
                id="HR-001",
                title="Product Owner review for release readiness",
                assigneeRole="Product Owner",
                reason="A lightweight human review confirms that the generated test scope matches business expectations.",
                approvalRequired=False,
            )
        )

    return tasks

