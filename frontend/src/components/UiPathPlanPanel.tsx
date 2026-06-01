import { Network } from "lucide-react";
import { assetTypeLabels, copy } from "../i18n";
import type { Language, UiPathOrchestrationPlan } from "../types/testPlan";

interface UiPathPlanPanelProps {
  plan: UiPathOrchestrationPlan;
  language: Language;
}

export function UiPathPlanPanel({ plan, language }: UiPathPlanPanelProps) {
  const t = copy[language];
  return (
    <section className="panel uipath-panel">
      <div className="panel-heading">
        <div>
          <p className="eyebrow">{t.executionLayer}</p>
          <h2>{t.uipathPlan}</h2>
        </div>
        <Network aria-hidden="true" size={24} />
      </div>

      <p className="summary-text">{plan.summary}</p>

      <div className="component-tags">
        {plan.components.map((component) => (
          <span key={component}>{component}</span>
        ))}
      </div>

      <div className="workflow">
        {plan.workflowSteps.map((step) => (
          <article key={step.step}>
            <div className="step-number">{step.step}</div>
            <div>
              <strong>{step.name}</strong>
              <span>{step.uipathComponent}</span>
              <p>{step.description}</p>
              <dl>
                <dt>{t.input}</dt>
                <dd>{step.input}</dd>
                <dt>{t.output}</dt>
                <dd>{step.output}</dd>
              </dl>
            </div>
          </article>
        ))}
      </div>

      <h3>{t.testCloudAssets}</h3>
      <div className="asset-grid">
        {plan.testCloudAssets.map((asset) => (
          <article key={`${asset.assetType}-${asset.name}`}>
            <span>{assetTypeLabels[language][asset.assetType] ?? asset.assetType}</span>
            <strong>{asset.name}</strong>
            <p>{asset.description}</p>
          </article>
        ))}
      </div>
    </section>
  );
}
