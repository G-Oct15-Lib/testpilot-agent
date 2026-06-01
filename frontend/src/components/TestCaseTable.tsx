import { automationLabels, copy, testTypeLabels } from "../i18n";
import type { Language, TestCase } from "../types/testPlan";
import { StatusBadge } from "./StatusBadge";

interface TestCaseTableProps {
  testCases: TestCase[];
  language: Language;
}

export function TestCaseTable({ testCases, language }: TestCaseTableProps) {
  const t = copy[language];
  return (
    <section className="panel">
      <div className="panel-heading">
        <div>
          <p className="eyebrow">{t.testAssets}</p>
          <h2>{t.testCases}</h2>
        </div>
      </div>

      <div className="table-wrap">
        <table>
          <thead>
            <tr>
              <th>{t.id}</th>
              <th>{t.title}</th>
              <th>{t.type}</th>
              <th>{t.priority}</th>
              <th>{t.risk}</th>
              <th>{t.automation}</th>
              <th>{t.mapping}</th>
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
                <td>{testTypeLabels[language][test.type]}</td>
                <td>
                  <StatusBadge value={test.priority} tone="priority" />
                </td>
                <td>
                  <StatusBadge value={test.riskLevel} language={language} />
                </td>
                <td>{test.automationCandidate ? t.candidate : t.manual}</td>
                <td>
                  <strong>{test.uipathTestCloudMapping.testSet}</strong>
                  <span>{automationLabels[language][test.uipathTestCloudMapping.automationType]}</span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}
