import { copy } from "../i18n";
import type { Language, RegressionRecommendation } from "../types/testPlan";
import { StatusBadge } from "./StatusBadge";

interface RegressionPanelProps {
  items: RegressionRecommendation[];
  language: Language;
}

export function RegressionPanel({ items, language }: RegressionPanelProps) {
  const t = copy[language];
  return (
    <section className="panel">
      <div className="panel-heading">
        <div>
          <p className="eyebrow">{t.coverage}</p>
          <h2>{t.regression}</h2>
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
