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


def test_llm_mode_uses_openai_compatible_chat_completion(monkeypatch) -> None:
    class FakeResponse:
        def raise_for_status(self) -> None:
            return None

        def json(self) -> dict:
            return {
                "choices": [
                    {
                        "message": {
                            "content": """
{
  "changeSummary": {
    "title": "Checkout payment timeout handling",
    "summary": "LLM-generated risk plan for checkout payment retry behavior.",
    "inputType": "pr_summary",
    "keyChanges": ["Payment retry behavior changed", "Order pending status changed"]
  },
  "impactAnalysis": {
    "affectedModules": [
      {"name": "Checkout", "impactLevel": "critical", "reason": "Checkout payment path changed."}
    ],
    "businessProcesses": ["Order-to-cash checkout flow"],
    "technicalAreas": ["Commerce workflow"]
  },
  "riskAssessment": {
    "overallRisk": "critical",
    "riskScore": 92,
    "riskFactors": [
      {"factor": "Payment retry", "severity": "critical", "explanation": "Duplicate charge risk."}
    ]
  },
  "testCases": [
    {
      "id": "TC-001",
      "title": "Validate payment retry timeout path",
      "type": "functional",
      "priority": "P0",
      "riskLevel": "critical",
      "steps": ["Trigger payment timeout", "Observe retry behavior"],
      "expectedResult": "Retry behavior is correct.",
      "automationCandidate": true,
      "uipathTestCloudMapping": {
        "testSet": "Checkout Release Readiness",
        "testCaseName": "Validate payment retry timeout path",
        "automationType": "hybrid"
      }
    },
    {
      "id": "TC-002",
      "title": "Validate duplicate charge prevention",
      "type": "regression",
      "priority": "P0",
      "riskLevel": "critical",
      "steps": ["Force gateway timeout", "Check charge records"],
      "expectedResult": "No duplicate charge is created.",
      "automationCandidate": true,
      "uipathTestCloudMapping": {
        "testSet": "Checkout Release Readiness",
        "testCaseName": "Validate duplicate charge prevention",
        "automationType": "automated"
      }
    },
    {
      "id": "TC-003",
      "title": "Validate failure messaging",
      "type": "smoke",
      "priority": "P1",
      "riskLevel": "critical",
      "steps": ["Simulate failed retry", "Read customer message"],
      "expectedResult": "The customer sees clear recovery guidance.",
      "automationCandidate": false,
      "uipathTestCloudMapping": {
        "testSet": "Checkout Release Readiness",
        "testCaseName": "Validate failure messaging",
        "automationType": "manual"
      }
    },
    {
      "id": "TC-004",
      "title": "Validate pending order status",
      "type": "integration",
      "priority": "P1",
      "riskLevel": "critical",
      "steps": ["Timeout payment", "Inspect order status"],
      "expectedResult": "Pending order is not cancelled too early.",
      "automationCandidate": true,
      "uipathTestCloudMapping": {
        "testSet": "Checkout Release Readiness",
        "testCaseName": "Validate pending order status",
        "automationType": "hybrid"
      }
    },
    {
      "id": "TC-005",
      "title": "Explore recovery paths",
      "type": "exploratory",
      "priority": "P1",
      "riskLevel": "critical",
      "steps": ["Try multiple timeout and retry combinations"],
      "expectedResult": "Recovery behavior is understandable.",
      "automationCandidate": false,
      "uipathTestCloudMapping": {
        "testSet": "Checkout Release Readiness",
        "testCaseName": "Explore recovery paths",
        "automationType": "manual"
      }
    }
  ],
  "regressionRecommendations": [
    {"module": "Checkout", "scenario": "Payment failure recovery", "reason": "Protect checkout conversion.", "priority": "P0"}
  ],
  "humanReviewTasks": [
    {"id": "HR-001", "title": "QA Lead approval", "assigneeRole": "QA Lead", "reason": "Critical payment flow.", "approvalRequired": true}
  ],
  "uipathOrchestrationPlan": {
    "summary": "Use UiPath Test Cloud and Action Center for governed release validation.",
    "components": ["UiPath Test Cloud / Test Manager", "UiPath Action Center"],
    "workflowSteps": [
      {"step": 1, "name": "Create test assets", "uipathComponent": "UiPath Test Cloud / Test Manager", "description": "Create draft test cases.", "input": "Test cases", "output": "Test Cloud drafts"}
    ],
    "testCloudAssets": [
      {"assetType": "Test Set", "name": "Checkout Release Readiness", "description": "Generated release test set."}
    ]
  }
}
"""
                        }
                    }
                ]
            }

    calls: list[dict] = []

    def fake_post(*args, **kwargs):
        calls.append({"args": args, "kwargs": kwargs})
        return FakeResponse()

    monkeypatch.setenv("TESTPILOT_AGENT_MODE", "llm")
    monkeypatch.setenv("TESTPILOT_LLM_API_KEY", "test-key")
    monkeypatch.setenv("TESTPILOT_LLM_BASE_URL", "https://llm.example/v1")
    monkeypatch.setenv("TESTPILOT_LLM_MODEL", "test-model")
    monkeypatch.setattr("app.agent.llm_client.httpx.post", fake_post)

    plan = generate_test_plan(
        AnalyzeRequest(
            inputType="pr_summary",
            title="Checkout payment timeout handling",
            businessContext="E-commerce checkout and payment workflow",
            content="This PR updates checkout payment retry handling when the payment gateway times out.",
        )
    )

    assert plan.agentMode == "llm"
    assert plan.riskAssessment.riskScore == 92
    assert calls[0]["args"][0] == "https://llm.example/v1/chat/completions"
    assert calls[0]["kwargs"]["json"]["model"] == "test-model"
    assert calls[0]["kwargs"]["headers"]["Authorization"] == "Bearer test-key"


def test_llm_mode_without_key_falls_back_to_mock(monkeypatch) -> None:
    monkeypatch.setenv("TESTPILOT_AGENT_MODE", "llm")
    monkeypatch.delenv("TESTPILOT_LLM_API_KEY", raising=False)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    plan = generate_test_plan(
        AnalyzeRequest(
            inputType="release_note",
            title="Profile page layout update",
            businessContext="Customer account profile",
            content="This release updates copy, style, layout, and form validation on the profile page.",
        )
    )

    assert plan.agentMode == "mock"
    assert len(plan.testCases) >= 5
