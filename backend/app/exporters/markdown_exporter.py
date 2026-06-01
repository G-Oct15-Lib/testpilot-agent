from __future__ import annotations

from app.models import TestPlanResponse


def export_markdown(plan: TestPlanResponse) -> str:
    lines: list[str] = [
        "# TestPilot Agent Test Plan",
        "",
        f"**Plan ID:** {plan.planId}",
        f"**Created At:** {plan.createdAt}",
        "",
        "## Change Summary",
        "",
        f"**Title:** {plan.changeSummary.title}",
        f"**Input Type:** {plan.changeSummary.inputType}",
        "",
        plan.changeSummary.summary,
        "",
        "### Key Changes",
    ]
    lines.extend(f"- {item}" for item in plan.changeSummary.keyChanges)

    lines.extend(["", "## Risk Assessment", ""])
    lines.append(f"**Overall Risk:** {plan.riskAssessment.overallRisk.upper()}")
    lines.append(f"**Risk Score:** {plan.riskAssessment.riskScore}/100")
    lines.append("")
    lines.append("### Risk Factors")
    lines.extend(
        f"- **{factor.severity.upper()}** {factor.factor}: {factor.explanation}"
        for factor in plan.riskAssessment.riskFactors
    )

    lines.extend(["", "## Affected Modules", ""])
    lines.extend(
        f"- **{module.name}** ({module.impactLevel}): {module.reason}"
        for module in plan.impactAnalysis.affectedModules
    )

    lines.extend(["", "## Generated Test Cases", ""])
    for test in plan.testCases:
        lines.extend(
            [
                f"### {test.id}: {test.title}",
                "",
                f"- Type: {test.type}",
                f"- Priority: {test.priority}",
                f"- Risk Level: {test.riskLevel}",
                f"- Automation Candidate: {'Yes' if test.automationCandidate else 'No'}",
                f"- UiPath Test Set: {test.uipathTestCloudMapping.testSet}",
                "",
                "**Steps:**",
            ]
        )
        lines.extend(f"{idx}. {step}" for idx, step in enumerate(test.steps, start=1))
        lines.extend(["", f"**Expected Result:** {test.expectedResult}", ""])

    lines.extend(["", "## Regression Recommendations", ""])
    lines.extend(
        f"- **{item.priority} {item.module}:** {item.scenario}. {item.reason}"
        for item in plan.regressionRecommendations
    )

    lines.extend(["", "## Human Review Tasks", ""])
    lines.extend(
        f"- **{task.assigneeRole}:** {task.title}. {task.reason}"
        for task in plan.humanReviewTasks
    )

    lines.extend(["", "## UiPath Integration Plan", "", plan.uipathOrchestrationPlan.summary, ""])
    lines.append("### Components")
    lines.extend(f"- {component}" for component in plan.uipathOrchestrationPlan.components)
    lines.extend(["", "### Workflow Steps"])
    for step in plan.uipathOrchestrationPlan.workflowSteps:
        lines.extend(
            [
                f"{step.step}. **{step.name}**",
                f"   - UiPath Component: {step.uipathComponent}",
                f"   - Description: {step.description}",
                f"   - Input: {step.input}",
                f"   - Output: {step.output}",
            ]
        )

    lines.extend(["", "## Release Readiness Notes", ""])
    if plan.riskAssessment.overallRisk in {"high", "critical"}:
        lines.append(
            "This release should not proceed until P0/P1 tests pass and required human approval tasks are completed."
        )
    else:
        lines.append("This release can proceed after standard smoke and regression checks pass.")

    return "\n".join(lines).strip() + "\n"

