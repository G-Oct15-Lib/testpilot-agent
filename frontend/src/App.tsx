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
import { copy } from "./i18n";
import type { AnalyzeRequest, ExampleScenario, Language, TestPlanResponse } from "./types/testPlan";

const initialRequest: AnalyzeRequest = {
  inputType: "pr_summary",
  title: "Checkout payment timeout handling",
  businessContext: "E-commerce checkout and payment workflow",
  content:
    "This PR updates the checkout payment retry logic. When the payment gateway times out, the system retries authorization up to two times before marking the payment as failed. It also changes the customer-facing error message and order status handling for pending payments.",
  language: "en"
};

const zhDemoRequest: AnalyzeRequest = {
  inputType: "pr_summary",
  title: "结账支付超时处理",
  businessContext: "电商结账和支付流程",
  content:
    "这个 PR 更新了结账支付重试逻辑。当支付网关超时时，系统会最多重试两次授权请求，然后才将付款标记为失败。它还调整了展示给客户的错误文案，并更新订单状态处理，避免待处理付款被过早取消。",
  language: "zh"
};

function App() {
  const [request, setRequest] = useState<AnalyzeRequest>(initialRequest);
  const [examples, setExamples] = useState<ExampleScenario[]>([]);
  const [language, setLanguage] = useState<Language>("en");
  const [plan, setPlan] = useState<TestPlanResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const t = copy[language];

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
    if (!plan) return t.waiting;
    if (plan.riskAssessment.overallRisk === "critical") return t.blocked;
    if (plan.riskAssessment.overallRisk === "high") return t.needsApproval;
    return t.ready;
  }, [plan, t]);

  const handleLanguageChange = (nextLanguage: Language) => {
    setLanguage(nextLanguage);
    setPlan(null);
    setError(null);
    setRequest((current) => {
      const isDemo = current.title === initialRequest.title || current.title === zhDemoRequest.title;
      if (isDemo) {
        return nextLanguage === "zh" ? zhDemoRequest : initialRequest;
      }
      return { ...current, language: nextLanguage };
    });
  };

  const handleLoadExample = (example: ExampleScenario) => {
    setPlan(null);
    setError(null);
    if (language === "zh" && example.id === "checkout-payment-risk") {
      setRequest(zhDemoRequest);
      return;
    }
    setRequest({ ...example, language });
  };

  const handleAnalyze = async () => {
    setLoading(true);
    setError(null);
    try {
      const result = await analyzeChange({ ...request, language });
      setPlan(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : t.analyzeError);
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
            <p>{t.track}</p>
            <h1>TestPilot Agent</h1>
          </div>
        </div>
        <div className="topbar-actions">
          <div className="language-switch" aria-label={t.languageLabel}>
            <button
              className={language === "en" ? "active" : ""}
              type="button"
              onClick={() => handleLanguageChange("en")}
            >
              {t.english}
            </button>
            <button
              className={language === "zh" ? "active" : ""}
              type="button"
              onClick={() => handleLanguageChange("zh")}
            >
              {t.chinese}
            </button>
          </div>
          <div className="status-pill">
            {plan ? <CheckCircle2 aria-hidden="true" size={18} /> : <CloudCog aria-hidden="true" size={18} />}
            {readinessLabel}
          </div>
        </div>
      </header>

      <main className="main-grid">
        <InputPanel
          value={request}
          examples={examples}
          language={language}
          loading={loading}
          onChange={setRequest}
          onAnalyze={handleAnalyze}
          onLoadExample={handleLoadExample}
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
              <h2>{t.emptyTitle}</h2>
              <p>{t.emptyBody}</p>
            </section>
          )}

          {plan && (
            <>
              <SummaryCards plan={plan} language={language} />
              <RiskPanel plan={plan} language={language} />
              <TestCaseTable testCases={plan.testCases} language={language} />
              <div className="side-by-side">
                <RegressionPanel items={plan.regressionRecommendations} language={language} />
                <HumanReviewPanel tasks={plan.humanReviewTasks} language={language} />
              </div>
              <UiPathPlanPanel plan={plan.uipathOrchestrationPlan} language={language} />
              <ExportActions plan={plan} language={language} />
            </>
          )}
        </div>
      </main>
    </div>
  );
}

export default App;
