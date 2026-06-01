from __future__ import annotations

from app.agent.keywords import MODULE_RULES, contains_any
from app.models import AffectedModule, AnalyzeRequest, ImpactAnalysis


LEVEL_ORDER = {"low": 0, "medium": 1, "high": 2, "critical": 3}


def _max_level(current: str, candidate: str) -> str:
    return candidate if LEVEL_ORDER[candidate] > LEVEL_ORDER[current] else current


def map_impact(request: AnalyzeRequest) -> ImpactAnalysis:
    text = f"{request.title}\n{request.businessContext or ''}\n{request.content}"
    modules: list[AffectedModule] = []
    business_processes: list[str] = []
    technical_areas: list[str] = []

    for rule in MODULE_RULES:
        matches = contains_any(text, rule.keywords)
        if not matches:
            continue

        impact_level = rule.default_level
        if {"payment", "checkout", "security", "permission", "delete", "production", "支付", "付款", "结账", "安全", "权限", "删除", "生产"} & set(matches):
            impact_level = _max_level(impact_level, "critical")

        modules.append(
            AffectedModule(
                name=rule.name,
                impactLevel=impact_level,  # type: ignore[arg-type]
                reason=f"{rule.reason} Matched signals: {', '.join(matches[:5])}.",
            )
        )
        business_processes.append(rule.business_process)
        technical_areas.append(rule.technical_area)

    if not modules:
        modules.append(
            AffectedModule(
                name="General Application Workflow",
                impactLevel="medium",
                reason="No specialized module keywords were detected, so the change should be tested through the main user workflow.",
            )
        )
        business_processes.append("General release validation")
        technical_areas.append("Application behavior")

    return ImpactAnalysis(
        affectedModules=modules,
        businessProcesses=list(dict.fromkeys(business_processes)),
        technicalAreas=list(dict.fromkeys(technical_areas)),
    )
