from __future__ import annotations

from app.models import (
    HumanReviewTask,
    TestCase,
    TestCloudAsset,
    UiPathOrchestrationPlan,
    WorkflowStep,
)


UIPATH_COMPONENTS = [
    "UiPath Test Cloud / Test Manager",
    "UiPath Orchestrator",
    "UiPath Robots",
    "UiPath Action Center",
    "UiPath Apps",
    "UiPath Integration Service",
    "UiPath API Workflows",
    "UiPath AI Agent / Autopilot-ready extension point",
]


def plan_uipath_orchestration(test_cases: list[TestCase], human_tasks: list[HumanReviewTask]) -> UiPathOrchestrationPlan:
    automated_count = sum(1 for case in test_cases if case.automationCandidate)
    manual_count = len(test_cases) - automated_count

    steps = [
        WorkflowStep(
            step=1,
            name="Receive change input from GitHub PR or release note",
            uipathComponent="UiPath API Workflow / Integration Service",
            description="Collect release context from GitHub, Jira, CI/CD, or a manual release note form.",
            input="PR summary, requirement, release note, or bugfix description",
            output="Normalized change payload for TestPilot Agent",
        ),
        WorkflowStep(
            step=2,
            name="Trigger TestPilot Agent analysis",
            uipathComponent="UiPath AI Agent / API Workflow",
            description="Invoke the analysis pipeline to generate risk, test cases, regression recommendations, and approval needs.",
            input="Normalized change payload",
            output="Structured TestPlanResponse JSON",
        ),
        WorkflowStep(
            step=3,
            name="Create or update test assets",
            uipathComponent="UiPath Test Cloud / Test Manager",
            description="Map generated test cases to Test Cloud test sets, cases, requirements, and test data.",
            input=f"{len(test_cases)} generated test cases",
            output="Test Cloud assets ready for execution and traceability",
        ),
        WorkflowStep(
            step=4,
            name="Launch automated regression tests",
            uipathComponent="UiPath Orchestrator + Robots",
            description="Run automation candidates through unattended or attended robots as part of release readiness.",
            input=f"{automated_count} automation candidates",
            output="Automated execution results linked back to Test Cloud",
        ),
        WorkflowStep(
            step=5,
            name="Route manual and approval tasks",
            uipathComponent="UiPath Action Center",
            description="Send high-risk manual checks and approval gates to the right human owner.",
            input=f"{manual_count} manual checks and {len(human_tasks)} review tasks",
            output="Approval or rejection decision with reviewer notes",
        ),
        WorkflowStep(
            step=6,
            name="Produce release readiness summary",
            uipathComponent="UiPath Apps / Dashboard / API Workflow",
            description="Combine AI analysis, test execution, and human decisions into a release readiness view.",
            input="Test Cloud results, Orchestrator job status, Action Center decisions",
            output="Go / no-go summary for release stakeholders",
        ),
    ]

    assets: list[TestCloudAsset] = [
        TestCloudAsset(
            assetType="Test Set",
            name=case.uipathTestCloudMapping.testSet,
            description="Generated release-readiness test set grouped by affected module and risk.",
        )
        for case in test_cases[:1]
    ]
    assets.extend(
        TestCloudAsset(
            assetType="Test Case",
            name=case.uipathTestCloudMapping.testCaseName,
            description=f"{case.priority} {case.type} case mapped as {case.uipathTestCloudMapping.automationType}.",
        )
        for case in test_cases[:6]
    )
    assets.append(
        TestCloudAsset(
            assetType="Requirement",
            name="Release readiness requirement",
            description="Traceability item connecting the source change to generated test coverage.",
        )
    )

    return UiPathOrchestrationPlan(
        summary=(
            "UiPath acts as the enterprise execution and orchestration layer: Test Cloud manages test assets, "
            "Orchestrator launches automation, Action Center keeps humans in the loop, and API Workflows connect "
            "release systems to the TestPilot Agent pipeline."
        ),
        components=UIPATH_COMPONENTS,
        workflowSteps=steps,
        testCloudAssets=assets,
    )

