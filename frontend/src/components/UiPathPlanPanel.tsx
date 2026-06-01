import { Network } from "lucide-react";
import type { UiPathOrchestrationPlan } from "../types/testPlan";

interface UiPathPlanPanelProps {
  plan: UiPathOrchestrationPlan;
}

export function UiPathPlanPanel({ plan }: UiPathPlanPanelProps) {
  return (
    <section className="panel uipath-panel">
      <div className="panel-heading">
        <div>
          <p className="eyebrow">Execution Layer</p>
          <h2>UiPath Integration Plan</h2>
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
                <dt>Input</dt>
                <dd>{step.input}</dd>
                <dt>Output</dt>
                <dd>{step.output}</dd>
              </dl>
            </div>
          </article>
        ))}
      </div>

      <h3>Test Cloud assets</h3>
      <div className="asset-grid">
        {plan.testCloudAssets.map((asset) => (
          <article key={`${asset.assetType}-${asset.name}`}>
            <span>{asset.assetType}</span>
            <strong>{asset.name}</strong>
            <p>{asset.description}</p>
          </article>
        ))}
      </div>
    </section>
  );
}

