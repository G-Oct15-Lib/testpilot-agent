from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field


InputType = Literal["pr_summary", "requirement", "release_note", "bugfix"]
Language = Literal["en", "zh"]
ImpactLevel = Literal["low", "medium", "high", "critical"]
TestType = Literal[
    "functional",
    "regression",
    "integration",
    "smoke",
    "security",
    "performance",
    "exploratory",
]
Priority = Literal["P0", "P1", "P2", "P3"]
AssigneeRole = Literal["QA Lead", "Release Manager", "Product Owner", "Security Reviewer"]
AssetType = Literal["Test Set", "Test Case", "Test Data", "Requirement", "Defect"]
AutomationType = Literal["manual", "automated", "hybrid"]


class AnalyzeRequest(BaseModel):
    inputType: InputType = "pr_summary"
    title: str = Field(..., min_length=3)
    content: str = Field(..., min_length=20)
    businessContext: Optional[str] = None
    language: Language = "en"


class ChangeSummary(BaseModel):
    title: str
    summary: str
    inputType: InputType
    keyChanges: list[str]


class AffectedModule(BaseModel):
    name: str
    impactLevel: ImpactLevel
    reason: str


class ImpactAnalysis(BaseModel):
    affectedModules: list[AffectedModule]
    businessProcesses: list[str]
    technicalAreas: list[str]


class RiskFactor(BaseModel):
    factor: str
    severity: ImpactLevel
    explanation: str


class RiskAssessment(BaseModel):
    overallRisk: ImpactLevel
    riskScore: int = Field(..., ge=0, le=100)
    riskFactors: list[RiskFactor]


class UiPathTestCloudMapping(BaseModel):
    testSet: str
    testCaseName: str
    automationType: AutomationType


class TestCase(BaseModel):
    id: str
    title: str
    type: TestType
    priority: Priority
    riskLevel: ImpactLevel
    steps: list[str]
    expectedResult: str
    automationCandidate: bool
    uipathTestCloudMapping: UiPathTestCloudMapping


class RegressionRecommendation(BaseModel):
    module: str
    scenario: str
    reason: str
    priority: Priority


class HumanReviewTask(BaseModel):
    id: str
    title: str
    assigneeRole: AssigneeRole
    reason: str
    approvalRequired: bool = True


class WorkflowStep(BaseModel):
    step: int
    name: str
    uipathComponent: str
    description: str
    input: str
    output: str


class TestCloudAsset(BaseModel):
    assetType: AssetType
    name: str
    description: str


class UiPathOrchestrationPlan(BaseModel):
    summary: str
    components: list[str]
    workflowSteps: list[WorkflowStep]
    testCloudAssets: list[TestCloudAsset]


class ExportLinks(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    markdown: Optional[str] = None
    json_link: Optional[str] = Field(default=None, alias="json")


class TestPlanResponse(BaseModel):
    language: Language = "en"
    planId: str
    createdAt: str
    changeSummary: ChangeSummary
    impactAnalysis: ImpactAnalysis
    riskAssessment: RiskAssessment
    testCases: list[TestCase]
    regressionRecommendations: list[RegressionRecommendation]
    humanReviewTasks: list[HumanReviewTask]
    uipathOrchestrationPlan: UiPathOrchestrationPlan
    exportLinks: ExportLinks = Field(default_factory=ExportLinks)


class ExampleScenario(BaseModel):
    id: str
    title: str
    inputType: InputType
    businessContext: str
    content: str


class ExportResponse(BaseModel):
    filename: str
    content: str
