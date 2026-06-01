import type { AnalyzeRequest, ExampleScenario, ExportResponse, TestPlanResponse } from "../types/testPlan";

const API_BASE = import.meta.env.VITE_API_BASE_URL ?? "";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...(init?.headers ?? {})
    },
    ...init
  });

  if (!response.ok) {
    const detail = await response.text();
    throw new Error(detail || `Request failed with ${response.status}`);
  }

  return response.json() as Promise<T>;
}

export function getExamples(): Promise<ExampleScenario[]> {
  return request<ExampleScenario[]>("/api/examples");
}

export function analyzeChange(payload: AnalyzeRequest): Promise<TestPlanResponse> {
  return request<TestPlanResponse>("/api/analyze", {
    method: "POST",
    body: JSON.stringify(payload)
  });
}

export function exportMarkdown(plan: TestPlanResponse): Promise<ExportResponse> {
  return request<ExportResponse>("/api/export/markdown", {
    method: "POST",
    body: JSON.stringify(plan)
  });
}

export function exportJson(plan: TestPlanResponse): Promise<ExportResponse> {
  return request<ExportResponse>("/api/export/json", {
    method: "POST",
    body: JSON.stringify(plan)
  });
}

