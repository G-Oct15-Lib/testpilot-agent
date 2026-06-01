export type InputType = "pr_summary" | "requirement" | "release_note" | "bugfix";
export type Language = "en" | "zh";
export type AgentMode = "mock" | "llm";
export type ImpactLevel = "low" | "medium" | "high" | "critical";
export type TestType =
  | "functional"
  | "regression"
  | "integration"
  | "smoke"
  | "security"
  | "performance"
  | "exploratory";
export type Priority = "P0" | "P1" | "P2" | "P3";
export type AutomationType = "manual" | "automated" | "hybrid";

export interface AnalyzeRequest {
  inputType: InputType;
  title: string;
  content: string;
  businessContext?: string;
  language?: Language;
}

export interface ExampleScenario extends AnalyzeRequest {
  id: string;
  businessContext: string;
}

export interface ChangeSummary {
  title: string;
  summary: string;
  inputType: InputType;
  keyChanges: string[];
}

export interface AffectedModule {
  name: string;
  impactLevel: ImpactLevel;
  reason: string;
}

export interface ImpactAnalysis {
  affectedModules: AffectedModule[];
  businessProcesses: string[];
  technicalAreas: string[];
}

export interface RiskFactor {
  factor: string;
  severity: ImpactLevel;
  explanation: string;
}

export interface RiskAssessment {
  overallRisk: ImpactLevel;
  riskScore: number;
  riskFactors: RiskFactor[];
}

export interface UiPathTestCloudMapping {
  testSet: string;
  testCaseName: string;
  automationType: AutomationType;
}

export interface TestCase {
  id: string;
  title: string;
  type: TestType;
  priority: Priority;
  riskLevel: ImpactLevel;
  steps: string[];
  expectedResult: string;
  automationCandidate: boolean;
  uipathTestCloudMapping: UiPathTestCloudMapping;
}

export interface RegressionRecommendation {
  module: string;
  scenario: string;
  reason: string;
  priority: Priority;
}

export interface HumanReviewTask {
  id: string;
  title: string;
  assigneeRole: string;
  reason: string;
  approvalRequired: boolean;
}

export interface WorkflowStep {
  step: number;
  name: string;
  uipathComponent: string;
  description: string;
  input: string;
  output: string;
}

export interface TestCloudAsset {
  assetType: string;
  name: string;
  description: string;
}

export interface UiPathOrchestrationPlan {
  summary: string;
  components: string[];
  workflowSteps: WorkflowStep[];
  testCloudAssets: TestCloudAsset[];
}

export interface TestPlanResponse {
  language: Language;
  agentMode: AgentMode;
  planId: string;
  createdAt: string;
  changeSummary: ChangeSummary;
  impactAnalysis: ImpactAnalysis;
  riskAssessment: RiskAssessment;
  testCases: TestCase[];
  regressionRecommendations: RegressionRecommendation[];
  humanReviewTasks: HumanReviewTask[];
  uipathOrchestrationPlan: UiPathOrchestrationPlan;
  exportLinks: {
    markdown?: string;
    json?: string;
  };
}

export interface ExportResponse {
  filename: string;
  content: string;
}
