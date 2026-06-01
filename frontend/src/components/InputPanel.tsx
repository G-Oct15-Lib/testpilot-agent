import { ClipboardList, PlayCircle, Sparkles } from "lucide-react";
import type { AnalyzeRequest, ExampleScenario, InputType } from "../types/testPlan";

interface InputPanelProps {
  value: AnalyzeRequest;
  examples: ExampleScenario[];
  loading: boolean;
  onChange: (value: AnalyzeRequest) => void;
  onAnalyze: () => void;
  onLoadExample: (example: ExampleScenario) => void;
}

const inputTypes: Array<{ label: string; value: InputType }> = [
  { label: "PR Summary", value: "pr_summary" },
  { label: "Product Requirement", value: "requirement" },
  { label: "Release Note", value: "release_note" },
  { label: "Bug Fix", value: "bugfix" }
];

export function InputPanel({ value, examples, loading, onChange, onAnalyze, onLoadExample }: InputPanelProps) {
  const update = (patch: Partial<AnalyzeRequest>) => onChange({ ...value, ...patch });

  return (
    <section className="panel input-panel">
      <div className="panel-heading">
        <div>
          <p className="eyebrow">Change Intake</p>
          <h2>Analyze release change</h2>
        </div>
        <ClipboardList aria-hidden="true" size={24} />
      </div>

      <label>
        Input type
        <select value={value.inputType} onChange={(event) => update({ inputType: event.target.value as InputType })}>
          {inputTypes.map((type) => (
            <option key={type.value} value={type.value}>
              {type.label}
            </option>
          ))}
        </select>
      </label>

      <label>
        Change title
        <input
          value={value.title}
          onChange={(event) => update({ title: event.target.value })}
          placeholder="Checkout payment timeout handling"
        />
      </label>

      <label>
        Business context
        <input
          value={value.businessContext ?? ""}
          onChange={(event) => update({ businessContext: event.target.value })}
          placeholder="E-commerce checkout and payment workflow"
        />
      </label>

      <label>
        Requirement, PR summary, release note, or bugfix
        <textarea
          value={value.content}
          onChange={(event) => update({ content: event.target.value })}
          placeholder="Paste the change description here..."
        />
      </label>

      <div className="example-row">
        {examples.map((example) => (
          <button className="secondary-button" key={example.id} type="button" onClick={() => onLoadExample(example)}>
            <PlayCircle aria-hidden="true" size={16} />
            {example.title}
          </button>
        ))}
      </div>

      <button className="primary-button" type="button" onClick={onAnalyze} disabled={loading}>
        <Sparkles aria-hidden="true" size={18} />
        {loading ? "Analyzing..." : "Analyze with TestPilot Agent"}
      </button>
    </section>
  );
}

