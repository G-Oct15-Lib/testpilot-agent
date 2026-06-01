#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
mkdir -p "$ROOT_DIR/samples"

TESTPILOT_ROOT="$ROOT_DIR" python3 - <<'PY'
import json
import os
from pathlib import Path
import sys

root = Path(os.environ["TESTPILOT_ROOT"])
sys.path.insert(0, str(root / "backend"))

from app.agent.pipeline import generate_test_plan
from app.models import AnalyzeRequest

request = AnalyzeRequest(
    inputType="pr_summary",
    title="Checkout payment timeout handling",
    businessContext="E-commerce checkout and payment workflow",
    content=(root / "samples" / "checkout-risky-change.txt").read_text(),
)
plan = generate_test_plan(request)
(root / "samples" / "generated-test-plan.example.json").write_text(
    json.dumps(plan.model_dump(by_alias=True), ensure_ascii=False, indent=2) + "\n"
)
PY
