import type { TestPlanResponse } from "../types/testPlan";
import { StatusBadge } from "./StatusBadge";

interface RiskPanelProps {
  plan: TestPlanResponse;
}

export function RiskPanel({ plan }: RiskPanelProps) {
  return (
    <section className="panel">
      <div className="panel-heading">
        <div>
          <p className="eyebrow">Agent Output</p>
          <h2>Risk and impact analysis</h2>
        </div>
        <StatusBadge value={plan.riskAssessment.overallRisk} />
      </div>

      <p className="summary-text">{plan.changeSummary.summary}</p>

      <div className="two-column">
        <div>
          <h3>Key changes</h3>
          <ul className="stack-list">
            {plan.changeSummary.keyChanges.map((change) => (
              <li key={change}>{change}</li>
            ))}
          </ul>
        </div>
        <div>
          <h3>Risk factors</h3>
          <ul className="stack-list">
            {plan.riskAssessment.riskFactors.map((factor) => (
              <li key={`${factor.factor}-${factor.severity}`}>
                <StatusBadge value={factor.severity} /> {factor.factor}
                <span>{factor.explanation}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>

      <h3>Affected modules</h3>
      <div className="module-grid">
        {plan.impactAnalysis.affectedModules.map((module) => (
          <article className="module-card" key={module.name}>
            <div>
              <strong>{module.name}</strong>
              <StatusBadge value={module.impactLevel} />
            </div>
            <p>{module.reason}</p>
          </article>
        ))}
      </div>
    </section>
  );
}

