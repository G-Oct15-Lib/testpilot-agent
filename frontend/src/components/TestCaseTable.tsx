import type { TestCase } from "../types/testPlan";
import { StatusBadge } from "./StatusBadge";

interface TestCaseTableProps {
  testCases: TestCase[];
}

export function TestCaseTable({ testCases }: TestCaseTableProps) {
  return (
    <section className="panel">
      <div className="panel-heading">
        <div>
          <p className="eyebrow">Test Cloud Assets</p>
          <h2>Generated test cases</h2>
        </div>
      </div>

      <div className="table-wrap">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Title</th>
              <th>Type</th>
              <th>Priority</th>
              <th>Risk</th>
              <th>Automation</th>
              <th>UiPath Test Cloud mapping</th>
            </tr>
          </thead>
          <tbody>
            {testCases.map((test) => (
              <tr key={test.id}>
                <td>{test.id}</td>
                <td>
                  <strong>{test.title}</strong>
                  <span>{test.expectedResult}</span>
                </td>
                <td>{test.type}</td>
                <td>
                  <StatusBadge value={test.priority} tone="priority" />
                </td>
                <td>
                  <StatusBadge value={test.riskLevel} />
                </td>
                <td>{test.automationCandidate ? "Candidate" : "Manual"}</td>
                <td>
                  <strong>{test.uipathTestCloudMapping.testSet}</strong>
                  <span>{test.uipathTestCloudMapping.automationType}</span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}

