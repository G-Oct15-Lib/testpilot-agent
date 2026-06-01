import { useEffect, useMemo, useState } from "react";
import { AlertTriangle, Bot, CheckCircle2, CloudCog } from "lucide-react";
import { analyzeChange, getExamples } from "./api/client";
import { ExportActions } from "./components/ExportActions";
import { HumanReviewPanel } from "./components/HumanReviewPanel";
import { InputPanel } from "./components/InputPanel";
import { RegressionPanel } from "./components/RegressionPanel";
import { RiskPanel } from "./components/RiskPanel";
import { SummaryCards } from "./components/SummaryCards";
import { TestCaseTable } from "./components/TestCaseTable";
import { UiPathPlanPanel } from "./components/UiPathPlanPanel";
import type { AnalyzeRequest, ExampleScenario, TestPlanResponse } from "./types/testPlan";

const initialRequest: AnalyzeRequest = {
  inputType: "pr_summary",
  title: "Checkout payment timeout handling",
  businessContext: "E-commerce checkout and payment workflow",
  content:
    "This PR updates the checkout payment retry logic. When the payment gateway times out, the system retries authorization up to two times before marking the payment as failed. It also changes the customer-facing error message and order status handling for pending payments."
};

function App() {
  const [request, setRequest] = useState<AnalyzeRequest>(initialRequest);
  const [examples, setExamples] = useState<ExampleScenario[]>([]);
  const [plan, setPlan] = useState<TestPlanResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    getExamples()
      .then((items) => {
        setExamples(items);
        if (items[0]) {
          setRequest(items[0]);
        }
      })
      .catch(() => {
        setExamples([]);
      });
  }, []);

  const readinessLabel = useMemo(() => {
    if (!plan) return "Waiting for change input";
    if (plan.riskAssessment.overallRisk === "critical") return "Release blocked until approval";
    if (plan.riskAssessment.overallRisk === "high") return "Release needs QA lead approval";
    return "Ready for standard validation";
  }, [plan]);

  const handleAnalyze = async () => {
    setLoading(true);
    setError(null);
    try {
      const result = await analyzeChange(request);
      setPlan(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to analyze this change.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-shell">
      <header className="topbar">
        <div className="brand">
          <div className="brand-mark">
            <Bot aria-hidden="true" size={26} />
          </div>
          <div>
            <p>UiPath AgentHack · Track 3: Test Cloud</p>
            <h1>TestPilot Agent</h1>
          </div>
        </div>
        <div className="status-pill">
          {plan ? <CheckCircle2 aria-hidden="true" size={18} /> : <CloudCog aria-hidden="true" size={18} />}
          {readinessLabel}
        </div>
      </header>

      <main className="main-grid">
        <InputPanel
          value={request}
          examples={examples}
          loading={loading}
          onChange={setRequest}
          onAnalyze={handleAnalyze}
          onLoadExample={(example) => setRequest(example)}
        />

        <div className="results-column">
          {error && (
            <section className="error-panel">
              <AlertTriangle aria-hidden="true" size={20} />
              <p>{error}</p>
            </section>
          )}

          {!plan && !error && (
            <section className="empty-state">
              <div>
                <CloudCog aria-hidden="true" size={34} />
              </div>
              <h2>Generate a risk-based test plan</h2>
              <p>
                Load the checkout scenario or paste a real release change. The local agent will create test cases,
                regression recommendations, human approval tasks, and a UiPath execution plan.
              </p>
            </section>
          )}

          {plan && (
            <>
              <SummaryCards plan={plan} />
              <RiskPanel plan={plan} />
              <TestCaseTable testCases={plan.testCases} />
              <div className="side-by-side">
                <RegressionPanel items={plan.regressionRecommendations} />
                <HumanReviewPanel tasks={plan.humanReviewTasks} />
              </div>
              <UiPathPlanPanel plan={plan.uipathOrchestrationPlan} />
              <ExportActions plan={plan} />
            </>
          )}
        </div>
      </main>
    </div>
  );
}

export default App;

