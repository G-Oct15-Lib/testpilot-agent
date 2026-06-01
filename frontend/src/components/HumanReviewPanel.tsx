import { UserCheck } from "lucide-react";
import type { HumanReviewTask } from "../types/testPlan";

interface HumanReviewPanelProps {
  tasks: HumanReviewTask[];
}

export function HumanReviewPanel({ tasks }: HumanReviewPanelProps) {
  return (
    <section className="panel">
      <div className="panel-heading">
        <div>
          <p className="eyebrow">Human-in-the-loop</p>
          <h2>Approval tasks</h2>
        </div>
        <UserCheck aria-hidden="true" size={24} />
      </div>
      <div className="review-list">
        {tasks.map((task) => (
          <article key={task.id}>
            <div className="review-avatar">{task.assigneeRole.slice(0, 2)}</div>
            <div>
              <strong>{task.title}</strong>
              <p>{task.reason}</p>
              <span>{task.assigneeRole} · {task.approvalRequired ? "Approval required" : "Review recommended"}</span>
            </div>
          </article>
        ))}
      </div>
    </section>
  );
}

