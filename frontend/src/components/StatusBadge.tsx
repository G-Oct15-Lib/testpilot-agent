import type { ImpactLevel, Priority } from "../types/testPlan";

interface StatusBadgeProps {
  value: ImpactLevel | Priority | string;
  tone?: "risk" | "priority" | "neutral";
}

export function StatusBadge({ value, tone = "risk" }: StatusBadgeProps) {
  const normalized = value.toLowerCase();
  const className = ["badge", tone, normalized.replace(/[^a-z0-9]+/g, "-")].join(" ");
  return <span className={className}>{value}</span>;
}

