from __future__ import annotations

from fastapi.testclient import TestClient

from app.agent.pipeline import generate_test_plan
from app.main import app
from app.models import AnalyzeRequest


def test_checkout_demo_generates_high_risk_test_plan() -> None:
    request = AnalyzeRequest(
        inputType="pr_summary",
        title="Checkout payment timeout handling",
        businessContext="E-commerce checkout and payment workflow",
        content=(
            "This PR updates checkout payment retry handling. When the payment gateway times out, "
            "the system retries authorization twice before marking the payment failed. It changes "
            "order status handling and customer-facing error messages."
        ),
    )

    plan = generate_test_plan(request)

    assert plan.planId.startswith("tp-")
    assert plan.riskAssessment.overallRisk in {"high", "critical"}
    assert plan.riskAssessment.riskScore >= 61
    assert len(plan.testCases) >= 5
    assert any(case.uipathTestCloudMapping.testSet for case in plan.testCases)
    assert any(task.approvalRequired for task in plan.humanReviewTasks)
    assert "UiPath Test Cloud / Test Manager" in plan.uipathOrchestrationPlan.components


def test_general_ui_change_still_gets_complete_plan() -> None:
    request = AnalyzeRequest(
        inputType="release_note",
        title="Profile page layout update",
        businessContext="Customer account profile",
        content="This release updates copy, style, layout, and form validation on the profile page.",
    )

    plan = generate_test_plan(request)

    assert len(plan.impactAnalysis.affectedModules) >= 1
    assert len(plan.testCases) >= 5
    assert len(plan.regressionRecommendations) >= 1


def test_api_analyze_and_export_roundtrip() -> None:
    client = TestClient(app)
    payload = {
        "inputType": "pr_summary",
        "title": "Checkout payment timeout handling",
        "businessContext": "E-commerce checkout and payment workflow",
        "content": (
            "This PR updates checkout payment retry handling. When the payment gateway times out, "
            "the system retries authorization twice before marking the payment failed."
        ),
    }

    analyze_response = client.post("/api/analyze", json=payload)
    assert analyze_response.status_code == 200
    plan = analyze_response.json()
    assert plan["riskAssessment"]["overallRisk"] in {"high", "critical"}
    assert plan["exportLinks"]["json"].startswith("/api/export/json")

    export_response = client.post("/api/export/markdown", json=plan)
    assert export_response.status_code == 200
    exported = export_response.json()
    assert exported["filename"].endswith(".md")
    assert "UiPath Integration Plan" in exported["content"]


def test_chinese_language_generates_localized_plan_and_export() -> None:
    client = TestClient(app)
    payload = {
        "inputType": "pr_summary",
        "title": "结账支付超时处理",
        "businessContext": "电商结账和支付流程",
        "content": (
            "这个 PR 更新了结账支付重试逻辑。当支付网关超时时，系统会最多重试两次授权请求，"
            "然后才将付款标记为失败。它还调整客户可见错误文案，并更新订单状态处理。"
        ),
        "language": "zh",
    }

    analyze_response = client.post("/api/analyze", json=payload)
    assert analyze_response.status_code == 200
    plan = analyze_response.json()
    assert plan["language"] == "zh"
    assert "结构化、基于风险的测试计划" in plan["changeSummary"]["summary"]
    assert any("支付" in module["name"] for module in plan["impactAnalysis"]["affectedModules"])
    assert plan["testCases"][0]["title"].startswith("冒烟验证")

    export_response = client.post("/api/export/markdown", json=plan)
    assert export_response.status_code == 200
    exported = export_response.json()
    assert "# TestPilot Agent 测试计划" in exported["content"]
