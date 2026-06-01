from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from app.agent.change_analyzer import analyze_change
from app.agent.human_review import plan_human_review
from app.agent.impact_mapper import map_impact
from app.agent.llm_client import try_generate_llm_plan
from app.agent.localizer import localize_plan
from app.agent.regression_recommender import recommend_regression
from app.agent.risk_scorer import score_risk
from app.agent.test_generator import generate_test_cases
from app.agent.uipath_planner import plan_uipath_orchestration
from app.models import AnalyzeRequest, ExportLinks, TestPlanResponse


def generate_test_plan(request: AnalyzeRequest) -> TestPlanResponse:
    llm_plan = try_generate_llm_plan(request)
    if llm_plan:
        return llm_plan

    change_summary = analyze_change(request)
    impact = map_impact(request)
    risk = score_risk(request.title, request.content, request.businessContext, impact)
    test_cases = generate_test_cases(request.title, impact, risk)
    regression = recommend_regression(impact)
    human_tasks = plan_human_review(impact, risk, test_cases)
    uipath_plan = plan_uipath_orchestration(test_cases, human_tasks)

    plan_id = f"tp-{uuid4().hex[:8]}"
    plan = TestPlanResponse(
        language=request.language,
        agentMode="mock",
        planId=plan_id,
        createdAt=datetime.now(timezone.utc).isoformat(),
        changeSummary=change_summary,
        impactAnalysis=impact,
        riskAssessment=risk,
        testCases=test_cases,
        regressionRecommendations=regression,
        humanReviewTasks=human_tasks,
        uipathOrchestrationPlan=uipath_plan,
        exportLinks=ExportLinks(
            markdown=f"/api/export/markdown?planId={plan_id}",
            json_link=f"/api/export/json?planId={plan_id}",
        ),
    )
    return localize_plan(plan, request)
