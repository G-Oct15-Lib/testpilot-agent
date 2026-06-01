import { riskLabels } from "../i18n";
import type { ImpactLevel, Language, Priority } from "../types/testPlan";

interface StatusBadgeProps {
  value: ImpactLevel | Priority | string;
  language?: Language;
  tone?: "risk" | "priority" | "neutral";
}

export function StatusBadge({ value, language = "en", tone = "risk" }: StatusBadgeProps) {
  const normalized = value.toLowerCase();
  const className = ["badge", tone, normalized.replace(/[^a-z0-9]+/g, "-")].join(" ");
  const label = tone === "risk" && value in riskLabels[language] ? riskLabels[language][value as ImpactLevel] : value;
  return <span className={className}>{label}</span>;
}
