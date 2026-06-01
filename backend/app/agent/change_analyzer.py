from __future__ import annotations

import re

from app.agent.keywords import CRITICAL_KEYWORDS, HIGH_KEYWORDS, MEDIUM_KEYWORDS, contains_any
from app.models import AnalyzeRequest, ChangeSummary


def _split_candidate_changes(content: str) -> list[str]:
    lines = [line.strip(" -\t") for line in content.splitlines() if line.strip()]
    candidates: list[str] = []
    for line in lines:
        if len(line) >= 12:
            candidates.append(line)

    if len(candidates) < 3:
        sentences = re.split(r"(?<=[.!?])\s+", content)
        candidates.extend(sentence.strip() for sentence in sentences if len(sentence.strip()) >= 20)

    return candidates


def analyze_change(request: AnalyzeRequest) -> ChangeSummary:
    text = f"{request.title}\n{request.businessContext or ''}\n{request.content}"
    candidates = _split_candidate_changes(request.content)
    important_keywords = contains_any(text, CRITICAL_KEYWORDS | HIGH_KEYWORDS | MEDIUM_KEYWORDS)

    key_changes = [
        candidate
        for candidate in candidates
        if any(keyword.lower() in candidate.lower() for keyword in important_keywords)
    ][:5]
    if not key_changes:
        key_changes = candidates[:4]
    if not key_changes:
        key_changes = ["Analyze the submitted change and create a risk-based testing plan."]

    normalized_type = request.inputType.replace("_", " ")
    keyword_summary = ", ".join(important_keywords[:5]) if important_keywords else "general application behavior"
    summary = (
        f"This {normalized_type} introduces changes related to {keyword_summary}. "
        "TestPilot Agent converted the raw change description into a structured, risk-based testing plan."
    )

    return ChangeSummary(
        title=request.title,
        summary=summary,
        inputType=request.inputType,
        keyChanges=key_changes,
    )

