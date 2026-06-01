from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.agent.pipeline import generate_test_plan
from app.examples import EXAMPLES
from app.exporters.json_exporter import export_json
from app.exporters.markdown_exporter import export_markdown
from app.models import AnalyzeRequest, ExampleScenario, ExportResponse, TestPlanResponse


app = FastAPI(
    title="TestPilot Agent API",
    description="Risk-based test orchestration assistant for UiPath AgentHack Track 3: Test Cloud.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "TestPilot Agent API"}


@app.get("/api/examples", response_model=list[ExampleScenario])
def examples() -> list[ExampleScenario]:
    return EXAMPLES


@app.post("/api/analyze", response_model=TestPlanResponse)
def analyze(request: AnalyzeRequest) -> TestPlanResponse:
    return generate_test_plan(request)


@app.post("/api/export/markdown", response_model=ExportResponse)
def export_plan_markdown(plan: TestPlanResponse) -> ExportResponse:
    safe_title = plan.changeSummary.title.lower().replace(" ", "-")[:40]
    return ExportResponse(filename=f"{safe_title or 'testpilot'}-test-plan.md", content=export_markdown(plan))


@app.post("/api/export/json", response_model=ExportResponse)
def export_plan_json(plan: TestPlanResponse) -> ExportResponse:
    safe_title = plan.changeSummary.title.lower().replace(" ", "-")[:40]
    return ExportResponse(filename=f"{safe_title or 'testpilot'}-test-plan.json", content=export_json(plan))

