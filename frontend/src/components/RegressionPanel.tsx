import type { RegressionRecommendation } from "../types/testPlan";
import { StatusBadge } from "./StatusBadge";

interface RegressionPanelProps {
  items: RegressionRecommendation[];
}

export function RegressionPanel({ items }: RegressionPanelProps) {
  return (
    <section className="panel">
      <div className="panel-heading">
        <div>
          <p className="eyebrow">Coverage Strategy</p>
          <h2>Regression recommendations</h2>
        </div>
      </div>
      <div className="recommendation-list">
        {items.map((item) => (
          <article key={`${item.module}-${item.scenario}`}>
            <StatusBadge value={item.priority} tone="priority" />
            <div>
              <strong>{item.module}: {item.scenario}</strong>
              <p>{item.reason}</p>
            </div>
          </article>
        ))}
      </div>
    </section>
  );
}

