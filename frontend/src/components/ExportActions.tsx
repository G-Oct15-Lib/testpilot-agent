import { Download, FileJson, FileText } from "lucide-react";
import { copy } from "../i18n";
import type { Language, TestPlanResponse } from "../types/testPlan";
import { exportJson, exportMarkdown } from "../api/client";

interface ExportActionsProps {
  plan: TestPlanResponse;
  language: Language;
}

function download(filename: string, content: string, mimeType: string) {
  const blob = new Blob([content], { type: mimeType });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = filename;
  link.click();
  URL.revokeObjectURL(url);
}

export function ExportActions({ plan, language }: ExportActionsProps) {
  const t = copy[language];
  const handleMarkdown = async () => {
    const result = await exportMarkdown(plan);
    download(result.filename, result.content, "text/markdown;charset=utf-8");
  };

  const handleJson = async () => {
    const result = await exportJson(plan);
    download(result.filename, result.content, "application/json;charset=utf-8");
  };

  return (
    <section className="export-bar">
      <div>
        <p className="eyebrow">{t.reportExport}</p>
        <strong>{t.downloadArtifacts}</strong>
      </div>
      <button className="secondary-button" type="button" onClick={handleMarkdown}>
        <FileText aria-hidden="true" size={16} />
        {t.exportMarkdown}
      </button>
      <button className="secondary-button" type="button" onClick={handleJson}>
        <FileJson aria-hidden="true" size={16} />
        {t.exportJson}
      </button>
      <Download aria-hidden="true" size={20} />
    </section>
  );
}
