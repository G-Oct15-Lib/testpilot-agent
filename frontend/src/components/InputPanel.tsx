import { ClipboardList, PlayCircle, Sparkles } from "lucide-react";
import { copy, exampleTitleLabels, inputTypeLabels } from "../i18n";
import type { AnalyzeRequest, ExampleScenario, InputType, Language } from "../types/testPlan";

interface InputPanelProps {
  value: AnalyzeRequest;
  examples: ExampleScenario[];
  language: Language;
  loading: boolean;
  onChange: (value: AnalyzeRequest) => void;
  onAnalyze: () => void;
  onLoadExample: (example: ExampleScenario) => void;
}

const inputTypes: InputType[] = ["pr_summary", "requirement", "release_note", "bugfix"];

export function InputPanel({ value, examples, language, loading, onChange, onAnalyze, onLoadExample }: InputPanelProps) {
  const update = (patch: Partial<AnalyzeRequest>) => onChange({ ...value, ...patch });
  const t = copy[language];

  return (
    <section className="panel input-panel">
      <div className="panel-heading">
        <div>
          <p className="eyebrow">{t.intakeEyebrow}</p>
          <h2>{t.intakeTitle}</h2>
        </div>
        <ClipboardList aria-hidden="true" size={24} />
      </div>

      <label>
        {t.inputType}
        <select value={value.inputType} onChange={(event) => update({ inputType: event.target.value as InputType })}>
          {inputTypes.map((type) => (
            <option key={type} value={type}>
              {inputTypeLabels[language][type]}
            </option>
          ))}
        </select>
      </label>

      <label>
        {t.changeTitle}
        <input
          value={value.title}
          onChange={(event) => update({ title: event.target.value })}
          placeholder={language === "zh" ? "结账支付超时处理" : "Checkout payment timeout handling"}
        />
      </label>

      <label>
        {t.businessContext}
        <input
          value={value.businessContext ?? ""}
          onChange={(event) => update({ businessContext: event.target.value })}
          placeholder={language === "zh" ? "电商结账和支付流程" : "E-commerce checkout and payment workflow"}
        />
      </label>

      <label>
        {t.contentLabel}
        <textarea
          value={value.content}
          onChange={(event) => update({ content: event.target.value })}
          placeholder={t.contentPlaceholder}
        />
      </label>

      <div className="example-row">
        {examples.map((example) => (
          <button className="secondary-button" key={example.id} type="button" onClick={() => onLoadExample(example)}>
            <PlayCircle aria-hidden="true" size={16} />
            {exampleTitleLabels[language][example.id] ?? example.title}
          </button>
        ))}
      </div>

      <button className="primary-button" type="button" onClick={onAnalyze} disabled={loading}>
        <Sparkles aria-hidden="true" size={18} />
        {loading ? t.analyzing : t.analyze}
      </button>
    </section>
  );
}
