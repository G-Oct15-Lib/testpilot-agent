import { copy } from "../i18n";
import type { Language, TestPlanResponse } from "../types/testPlan";
import { StatusBadge } from "./StatusBadge";

interface RiskPanelProps {
  plan: TestPlanResponse;
  language: Language;
}

export function RiskPanel({ plan, language }: RiskPanelProps) {
  const t = copy[language];
  return (
    <section className="panel">
      <div className="panel-heading">
        <div>
          <p className="eyebrow">{t.agentOutput}</p>
          <h2>{t.riskImpact}</h2>
        </div>
        <StatusBadge value={plan.riskAssessment.overallRisk} language={language} />
      </div>

      <p className="summary-text">{plan.changeSummary.summary}</p>

      <div className="two-column">
        <div>
          <h3>{t.keyChanges}</h3>
          <ul className="stack-list">
            {plan.changeSummary.keyChanges.map((change) => (
              <li key={change}>{change}</li>
            ))}
          </ul>
        </div>
        <div>
          <h3>{t.riskFactors}</h3>
          <ul className="stack-list">
            {plan.riskAssessment.riskFactors.map((factor) => (
              <li key={`${factor.factor}-${factor.severity}`}>
                <StatusBadge value={factor.severity} language={language} /> {factor.factor}
                <span>{factor.explanation}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>

      <h3>{t.affectedModules}</h3>
      <div className="module-grid">
        {plan.impactAnalysis.affectedModules.map((module) => (
          <article className="module-card" key={module.name}>
            <div>
              <strong>{module.name}</strong>
              <StatusBadge value={module.impactLevel} language={language} />
            </div>
            <p>{module.reason}</p>
          </article>
        ))}
      </div>
    </section>
  );
}
