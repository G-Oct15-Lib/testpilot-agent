from __future__ import annotations

from app.models import ImpactAnalysis, RiskAssessment, TestCase, UiPathTestCloudMapping


def _priority_for_risk(risk: str, index: int) -> str:
    if risk == "critical":
        return "P0" if index <= 2 else "P1"
    if risk == "high":
        return "P1" if index <= 4 else "P2"
    if risk == "medium":
        return "P2"
    return "P3"


def _mapping(title: str, test_set: str, automation_type: str) -> UiPathTestCloudMapping:
    return UiPathTestCloudMapping(
        testSet=test_set,
        testCaseName=title,
        automationType=automation_type,  # type: ignore[arg-type]
    )


def generate_test_cases(title: str, impact: ImpactAnalysis, risk: RiskAssessment) -> list[TestCase]:
    primary_module = impact.affectedModules[0].name
    overall = risk.overallRisk
    test_set = f"{primary_module} Release Readiness"

    templates = [
        (
            "smoke",
            f"Smoke validate {primary_module} critical path",
            [
                "Open the application in a production-like test environment.",
                f"Complete the main {primary_module.lower()} workflow with valid data.",
                "Verify the user reaches the expected success state without blocking errors.",
            ],
            "The main workflow remains available after the change.",
            "automated",
        ),
        (
            "functional",
            f"Verify changed behavior for {title}",
            [
                "Prepare test data that exercises the changed behavior.",
                "Execute the updated path described in the change summary.",
                "Compare the actual behavior with the release requirement.",
            ],
            "The changed behavior matches the requirement and does not introduce incorrect states.",
            "hybrid",
        ),
        (
            "regression",
            f"Regression cover neighboring {primary_module} scenarios",
            [
                "Run existing regression scenarios for the affected module.",
                "Include adjacent success, failure, and retry paths.",
                "Check that previous behavior remains backward compatible.",
            ],
            "Existing supported scenarios still pass after the release change.",
            "automated",
        ),
        (
            "integration",
            "Validate downstream integration contracts",
            [
                "Trigger the changed workflow through the public API or integration boundary.",
                "Inspect request, response, and state transition data.",
                "Confirm that dependent services receive compatible data.",
            ],
            "External and downstream integrations remain compatible with the change.",
            "automated",
        ),
        (
            "exploratory",
            "Explore high-risk exception and recovery paths",
            [
                "Force timeout, validation, or failure conditions from the risk assessment.",
                "Observe customer-facing messaging and internal status updates.",
                "Document any behavior that requires product or release manager review.",
            ],
            "Unexpected failures are handled clearly and recoverably.",
            "manual",
        ),
    ]

    if overall in {"high", "critical"}:
        templates.append(
            (
                "security" if any("security" in factor.factor.lower() for factor in risk.riskFactors) else "functional",
                "Approval gate for high-risk release decision",
                [
                    "Review generated P0/P1 cases with QA Lead and Release Manager.",
                    "Confirm whether all automated and manual gates are satisfied.",
                    "Record approval or rollback recommendation before release.",
                ],
                "A human owner explicitly approves or blocks the high-risk release.",
                "manual",
            )
        )

    cases: list[TestCase] = []
    for index, (case_type, case_title, steps, expected, automation_type) in enumerate(templates, start=1):
        priority = _priority_for_risk(overall, index)
        cases.append(
            TestCase(
                id=f"TC-{index:03d}",
                title=case_title,
                type=case_type,  # type: ignore[arg-type]
                priority=priority,  # type: ignore[arg-type]
                riskLevel=overall,
                steps=steps,
                expectedResult=expected,
                automationCandidate=automation_type in {"automated", "hybrid"},
                uipathTestCloudMapping=_mapping(case_title, test_set, automation_type),
            )
        )

    return cases

