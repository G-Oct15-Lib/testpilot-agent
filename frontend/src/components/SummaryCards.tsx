import { Activity, GitBranch, ShieldCheck } from "lucide-react";
import type { TestPlanResponse } from "../types/testPlan";
import { StatusBadge } from "./StatusBadge";

interface SummaryCardsProps {
  plan: TestPlanResponse;
}

export function SummaryCards({ plan }: SummaryCardsProps) {
  return (
    <div className="summary-grid">
      <article className="metric-card">
        <div className="metric-icon">
          <ShieldCheck aria-hidden="true" size={20} />
        </div>
        <p>Overall risk</p>
        <h3>{plan.riskAssessment.riskScore}/100</h3>
        <StatusBadge value={plan.riskAssessment.overallRisk} />
      </article>

      <article className="metric-card">
        <div className="metric-icon">
          <GitBranch aria-hidden="true" size={20} />
        </div>
        <p>Affected modules</p>
        <h3>{plan.impactAnalysis.affectedModules.length}</h3>
        <span>{plan.impactAnalysis.technicalAreas.slice(0, 2).join(", ")}</span>
      </article>

      <article className="metric-card">
        <div className="metric-icon">
          <Activity aria-hidden="true" size={20} />
        </div>
        <p>Generated tests</p>
        <h3>{plan.testCases.length}</h3>
        <span>{plan.testCases.filter((test) => test.automationCandidate).length} automation candidates</span>
      </article>
    </div>
  );
}

