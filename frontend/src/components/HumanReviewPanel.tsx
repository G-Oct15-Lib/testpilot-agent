import { UserCheck } from "lucide-react";
import { copy, roleLabels } from "../i18n";
import type { HumanReviewTask, Language } from "../types/testPlan";

interface HumanReviewPanelProps {
  tasks: HumanReviewTask[];
  language: Language;
}

export function HumanReviewPanel({ tasks, language }: HumanReviewPanelProps) {
  const t = copy[language];
  const roleName = (role: string) => roleLabels[language][role] ?? role;
  return (
    <section className="panel">
      <div className="panel-heading">
        <div>
          <p className="eyebrow">{t.humanLoop}</p>
          <h2>{t.approvalTasks}</h2>
        </div>
        <UserCheck aria-hidden="true" size={24} />
      </div>
      <div className="review-list">
        {tasks.map((task) => (
          <article key={task.id}>
            <div className="review-avatar">{roleName(task.assigneeRole).slice(0, 2)}</div>
            <div>
              <strong>{task.title}</strong>
              <p>{task.reason}</p>
              <span>
                {roleName(task.assigneeRole)} · {task.approvalRequired ? t.approvalRequired : t.reviewRecommended}
              </span>
            </div>
          </article>
        ))}
      </div>
    </section>
  );
}
