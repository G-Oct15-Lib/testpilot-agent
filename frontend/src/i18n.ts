import type { AutomationType, ImpactLevel, InputType, Language, TestType } from "./types/testPlan";

export const copy = {
  en: {
    track: "UiPath AgentHack · Track 3: Test Cloud",
    waiting: "Waiting for change input",
    blocked: "Release blocked until approval",
    needsApproval: "Release needs QA lead approval",
    ready: "Ready for standard validation",
    emptyTitle: "Generate a risk-based test plan",
    emptyBody:
      "Load the checkout scenario or paste a real release change. The local agent will create test cases, regression recommendations, human approval tasks, and a UiPath execution plan.",
    analyzeError: "Unable to analyze this change.",
    languageLabel: "Language",
    english: "English",
    chinese: "中文",
    intakeEyebrow: "Change Intake",
    intakeTitle: "Analyze release change",
    inputType: "Input type",
    changeTitle: "Change title",
    businessContext: "Business context",
    contentLabel: "Requirement, PR summary, release note, or bugfix",
    contentPlaceholder: "Paste the change description here...",
    analyze: "Analyze with TestPilot Agent",
    analyzing: "Analyzing...",
    agentOutput: "Agent Output",
    riskImpact: "Risk and impact analysis",
    keyChanges: "Key changes",
    riskFactors: "Risk factors",
    affectedModules: "Affected modules",
    overallRisk: "Overall risk",
    modules: "Affected modules",
    generatedTests: "Generated tests",
    automationCandidates: "automation candidates",
    mockMode: "mock mode",
    llmMode: "LLM mode",
    testAssets: "Test Cloud Assets",
    testCases: "Generated test cases",
    id: "ID",
    title: "Title",
    type: "Type",
    priority: "Priority",
    risk: "Risk",
    automation: "Automation",
    mapping: "UiPath Test Cloud mapping",
    candidate: "Candidate",
    manual: "Manual",
    coverage: "Coverage Strategy",
    regression: "Regression recommendations",
    humanLoop: "Human-in-the-loop",
    approvalTasks: "Approval tasks",
    approvalRequired: "Approval required",
    reviewRecommended: "Review recommended",
    executionLayer: "Execution Layer",
    uipathPlan: "UiPath Integration Plan",
    input: "Input",
    output: "Output",
    testCloudAssets: "Test Cloud assets",
    reportExport: "Report Export",
    downloadArtifacts: "Download judge-ready artifacts",
    exportMarkdown: "Export Markdown",
    exportJson: "Export JSON",
  },
  zh: {
    track: "UiPath AgentHack · 赛道 3：Test Cloud",
    waiting: "等待输入变更内容",
    blocked: "发布需审批后才能继续",
    needsApproval: "发布需要 QA 负责人审批",
    ready: "可进入标准验证",
    emptyTitle: "生成基于风险的测试计划",
    emptyBody:
      "加载结账示例或粘贴真实发布变更。本地 Agent 会生成测试用例、回归建议、人工审批任务和 UiPath 执行方案。",
    analyzeError: "无法分析这个变更。",
    languageLabel: "语言",
    english: "English",
    chinese: "中文",
    intakeEyebrow: "变更输入",
    intakeTitle: "分析发布变更",
    inputType: "输入类型",
    changeTitle: "变更标题",
    businessContext: "业务背景",
    contentLabel: "需求、PR 摘要、发布说明或缺陷修复",
    contentPlaceholder: "在这里粘贴变更描述...",
    analyze: "使用 TestPilot Agent 分析",
    analyzing: "分析中...",
    agentOutput: "Agent 输出",
    riskImpact: "风险和影响分析",
    keyChanges: "关键变化",
    riskFactors: "风险因素",
    affectedModules: "受影响模块",
    overallRisk: "总体风险",
    modules: "受影响模块",
    generatedTests: "生成测试",
    automationCandidates: "个自动化候选",
    mockMode: "mock 模式",
    llmMode: "真实模型模式",
    testAssets: "Test Cloud 资产",
    testCases: "生成的测试用例",
    id: "ID",
    title: "标题",
    type: "类型",
    priority: "优先级",
    risk: "风险",
    automation: "自动化",
    mapping: "UiPath Test Cloud 映射",
    candidate: "候选",
    manual: "手工",
    coverage: "覆盖策略",
    regression: "回归建议",
    humanLoop: "人工闭环",
    approvalTasks: "审批任务",
    approvalRequired: "需要审批",
    reviewRecommended: "建议复核",
    executionLayer: "执行层",
    uipathPlan: "UiPath 集成方案",
    input: "输入",
    output: "输出",
    testCloudAssets: "Test Cloud 资产",
    reportExport: "报告导出",
    downloadArtifacts: "下载评审材料",
    exportMarkdown: "导出 Markdown",
    exportJson: "导出 JSON",
  },
} as const;

export const inputTypeLabels: Record<Language, Record<InputType, string>> = {
  en: {
    pr_summary: "PR Summary",
    requirement: "Product Requirement",
    release_note: "Release Note",
    bugfix: "Bug Fix",
  },
  zh: {
    pr_summary: "PR 摘要",
    requirement: "产品需求",
    release_note: "发布说明",
    bugfix: "缺陷修复",
  },
};

export const riskLabels: Record<Language, Record<ImpactLevel, string>> = {
  en: {
    low: "low",
    medium: "medium",
    high: "high",
    critical: "critical",
  },
  zh: {
    low: "低",
    medium: "中",
    high: "高",
    critical: "严重",
  },
};

export const testTypeLabels: Record<Language, Record<TestType, string>> = {
  en: {
    functional: "functional",
    regression: "regression",
    integration: "integration",
    smoke: "smoke",
    security: "security",
    performance: "performance",
    exploratory: "exploratory",
  },
  zh: {
    functional: "功能",
    regression: "回归",
    integration: "集成",
    smoke: "冒烟",
    security: "安全",
    performance: "性能",
    exploratory: "探索",
  },
};

export const automationLabels: Record<Language, Record<AutomationType, string>> = {
  en: {
    manual: "manual",
    automated: "automated",
    hybrid: "hybrid",
  },
  zh: {
    manual: "手工",
    automated: "自动化",
    hybrid: "混合",
  },
};

export const roleLabels: Record<Language, Record<string, string>> = {
  en: {},
  zh: {
    "QA Lead": "QA 负责人",
    "Release Manager": "发布经理",
    "Product Owner": "产品负责人",
    "Security Reviewer": "安全负责人",
  },
};

export const assetTypeLabels: Record<Language, Record<string, string>> = {
  en: {},
  zh: {
    "Test Set": "测试集",
    "Test Case": "测试用例",
    "Test Data": "测试数据",
    Requirement: "需求",
    Defect: "缺陷",
  },
};

export const exampleTitleLabels: Record<Language, Record<string, string>> = {
  en: {},
  zh: {
    "checkout-payment-risk": "结账支付超时处理",
    "auth-role-policy": "角色权限策略更新",
    "invoice-export-bugfix": "发票导出超时修复",
  },
};

export function labelFor<T extends string>(map: Record<Language, Record<T, string>>, language: Language, value: T) {
  return map[language][value] ?? value;
}
