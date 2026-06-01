from __future__ import annotations

import json

from app.models import TestPlanResponse


def export_json(plan: TestPlanResponse) -> str:
    return json.dumps(plan.model_dump(by_alias=True), ensure_ascii=False, indent=2)
