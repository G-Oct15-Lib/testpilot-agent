import { Activity, GitBranch, ShieldCheck } from "lucide-react";
import { copy } from "../i18n";
import type { Language, TestPlanResponse } from "../types/testPlan";
import { StatusBadge } from "./StatusBadge";

interface SummaryCardsProps {
  plan: TestPlanResponse;
  language: Language;
}

export function SummaryCards({ plan, language }: SummaryCardsProps) {
  const t = copy[language];
  return (
    <div className="summary-grid">
      <article className="metric-card">
        <div className="metric-icon">
          <ShieldCheck aria-hidden="true" size={20} />
        </div>
        <p>{t.overallRisk}</p>
        <h3>{plan.riskAssessment.riskScore}/100</h3>
        <StatusBadge value={plan.riskAssessment.overallRisk} language={language} />
      </article>

      <article className="metric-card">
        <div className="metric-icon">
          <GitBranch aria-hidden="true" size={20} />
        </div>
        <p>{t.modules}</p>
        <h3>{plan.impactAnalysis.affectedModules.length}</h3>
        <span>{plan.impactAnalysis.technicalAreas.slice(0, 2).join(", ")}</span>
      </article>

      <article className="metric-card">
        <div className="metric-icon">
          <Activity aria-hidden="true" size={20} />
        </div>
        <p>{t.generatedTests}</p>
        <h3>{plan.testCases.length}</h3>
        <span>
          {plan.testCases.filter((test) => test.automationCandidate).length} {t.automationCandidates} ·{" "}
          {plan.agentMode === "llm" ? t.llmMode : t.mockMode}
        </span>
      </article>
    </div>
  );
}
