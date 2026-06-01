from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Optional
from uuid import uuid4

import httpx

from app.models import AnalyzeRequest, ExportLinks, TestPlanResponse


SUPPORTED_MODES = {"mock", "auto", "llm"}


@dataclass(frozen=True)
class LLMConfig:
    mode: str
    api_key: Optional[str]
    base_url: str
    model: str
    timeout_seconds: float
    strict: bool


def get_llm_config() -> LLMConfig:
    mode = os.getenv("TESTPILOT_AGENT_MODE", "mock").strip().lower()
    if mode not in SUPPORTED_MODES:
        mode = "mock"

    return LLMConfig(
        mode=mode,
        api_key=os.getenv("TESTPILOT_LLM_API_KEY") or os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("TESTPILOT_LLM_BASE_URL", "https://api.openai.com/v1").rstrip("/"),
        model=os.getenv("TESTPILOT_LLM_MODEL", "gpt-4o-mini"),
        timeout_seconds=float(os.getenv("TESTPILOT_LLM_TIMEOUT_SECONDS", "35")),
        strict=os.getenv("TESTPILOT_LLM_STRICT", "false").strip().lower() in {"1", "true", "yes"},
    )


def try_generate_llm_plan(request: AnalyzeRequest) -> Optional[TestPlanResponse]:
    config = get_llm_config()
    if config.mode == "mock" or not config.api_key:
        return None

    try:
        return _generate_llm_plan(request, config)
    except Exception:
        if config.strict:
            raise
        return None


def _generate_llm_plan(request: AnalyzeRequest, config: LLMConfig) -> TestPlanResponse:
    response = httpx.post(
        f"{config.base_url}/chat/completions",
        headers={
            "Authorization": f"Bearer {config.api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": config.model,
            "temperature": 0.2,
            "response_format": {"type": "json_object"},
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are TestPilot Agent, an enterprise QA planning assistant for UiPath Test Cloud. "
                        "Return only valid JSON. Do not wrap JSON in Markdown."
                    ),
                },
                {"role": "user", "content": _build_prompt(request)},
            ],
        },
        timeout=config.timeout_seconds,
    )
    response.raise_for_status()
    completion = response.json()
    content = completion["choices"][0]["message"]["content"]
    payload = _extract_json(content)
    return _build_plan(request, payload)


def _build_prompt(request: AnalyzeRequest) -> str:
    output_language = "Simplified Chinese" if request.language == "zh" else "English"
    return f"""
Analyze this release change and generate a risk-based test orchestration plan for UiPath Test Cloud.

Target language for human-readable text: {output_language}.
Keep enum values in English exactly as requested.

Input:
- inputType: {request.inputType}
- title: {request.title}
- businessContext: {request.businessContext or "N/A"}
- content:
{request.content}

Return a JSON object with exactly these top-level fields:
- changeSummary
- impactAnalysis
- riskAssessment
- testCases
- regressionRecommendations
- humanReviewTasks
- uipathOrchestrationPlan

Required shape:
{{
  "changeSummary": {{
    "title": "string",
    "summary": "string",
    "inputType": "{request.inputType}",
    "keyChanges": ["string"]
  }},
  "impactAnalysis": {{
    "affectedModules": [
      {{"name": "string", "impactLevel": "low|medium|high|critical", "reason": "string"}}
    ],
    "businessProcesses": ["string"],
    "technicalAreas": ["string"]
  }},
  "riskAssessment": {{
    "overallRisk": "low|medium|high|critical",
    "riskScore": 0,
    "riskFactors": [
      {{"factor": "string", "severity": "low|medium|high|critical", "explanation": "string"}}
    ]
  }},
  "testCases": [
    {{
      "id": "TC-001",
      "title": "string",
      "type": "functional|regression|integration|smoke|security|performance|exploratory",
      "priority": "P0|P1|P2|P3",
      "riskLevel": "low|medium|high|critical",
      "steps": ["string"],
      "expectedResult": "string",
      "automationCandidate": true,
      "uipathTestCloudMapping": {{
        "testSet": "string",
        "testCaseName": "string",
        "automationType": "manual|automated|hybrid"
      }}
    }}
  ],
  "regressionRecommendations": [
    {{"module": "string", "scenario": "string", "reason": "string", "priority": "P0|P1|P2|P3"}}
  ],
  "humanReviewTasks": [
    {{
      "id": "HR-001",
      "title": "string",
      "assigneeRole": "QA Lead|Release Manager|Product Owner|Security Reviewer",
      "reason": "string",
      "approvalRequired": true
    }}
  ],
  "uipathOrchestrationPlan": {{
    "summary": "string",
    "components": ["UiPath Test Cloud / Test Manager", "UiPath Orchestrator"],
    "workflowSteps": [
      {{
        "step": 1,
        "name": "string",
        "uipathComponent": "string",
        "description": "string",
        "input": "string",
        "output": "string"
      }}
    ],
    "testCloudAssets": [
      {{"assetType": "Test Set|Test Case|Test Data|Requirement|Defect", "name": "string", "description": "string"}}
    ]
  }}
}}

Rules:
- Generate 5 to 7 test cases.
- Include at least one UiPath Test Cloud test set and one Action Center-style human review task.
- Use riskScore as an integer from 0 to 100.
- Do not include planId, createdAt, language, agentMode, or exportLinks.
""".strip()


def _extract_json(content: str) -> dict[str, Any]:
    stripped = content.strip()
    if stripped.startswith("```"):
        stripped = re.sub(r"^```(?:json)?\s*", "", stripped)
        stripped = re.sub(r"\s*```$", "", stripped)
    parsed = json.loads(stripped)
    if not isinstance(parsed, dict):
        raise ValueError("LLM response must be a JSON object.")
    return parsed


def _build_plan(request: AnalyzeRequest, payload: dict[str, Any]) -> TestPlanResponse:
    plan_id = f"tp-{uuid4().hex[:8]}"
    payload = {
        **payload,
        "language": request.language,
        "agentMode": "llm",
        "planId": plan_id,
        "createdAt": datetime.now(timezone.utc).isoformat(),
        "exportLinks": {
            "markdown": f"/api/export/markdown?planId={plan_id}",
            "json": f"/api/export/json?planId={plan_id}",
        },
    }
    return TestPlanResponse.model_validate(payload)
