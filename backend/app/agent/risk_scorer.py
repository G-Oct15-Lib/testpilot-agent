from __future__ import annotations

from typing import Optional

from app.agent.keywords import CRITICAL_KEYWORDS, HIGH_KEYWORDS, LOW_KEYWORDS, MEDIUM_KEYWORDS, contains_any
from app.models import ImpactAnalysis, RiskAssessment, RiskFactor


LEVEL_POINTS = {"low": 4, "medium": 8, "high": 14, "critical": 22}


def _overall(score: int) -> str:
    if score >= 81:
        return "critical"
    if score >= 61:
        return "high"
    if score >= 31:
        return "medium"
    return "low"


def score_risk(title: str, content: str, business_context: Optional[str], impact: ImpactAnalysis) -> RiskAssessment:
    text = f"{title}\n{business_context or ''}\n{content}"
    score = 10
    factors: list[RiskFactor] = []

    keyword_sets = [
        ("critical business or security keyword", "critical", CRITICAL_KEYWORDS, 18),
        ("failure or integration keyword", "high", HIGH_KEYWORDS, 11),
        ("workflow or validation keyword", "medium", MEDIUM_KEYWORDS, 6),
        ("copy or layout keyword", "low", LOW_KEYWORDS, 2),
    ]
    for label, severity, keywords, points in keyword_sets:
        matches = contains_any(text, keywords)
        if matches:
            score += min(len(matches) * points, points * 3)
            factors.append(
                RiskFactor(
                    factor=f"Detected {label}",
                    severity=severity,  # type: ignore[arg-type]
                    explanation=f"Matched signals: {', '.join(matches[:6])}.",
                )
            )

    for module in impact.affectedModules:
        score += LEVEL_POINTS[module.impactLevel]

    if len(impact.affectedModules) >= 3:
        score += 10
        factors.append(
            RiskFactor(
                factor="Multiple affected modules",
                severity="high",
                explanation="The change crosses multiple modules, increasing regression and orchestration risk.",
            )
        )

    if not factors:
        factors.append(
            RiskFactor(
                factor="General release uncertainty",
                severity="medium",
                explanation="The change still needs baseline smoke, functional, and regression validation.",
            )
        )

    score = max(0, min(score, 100))
    return RiskAssessment(overallRisk=_overall(score), riskScore=score, riskFactors=factors)  # type: ignore[arg-type]
