from __future__ import annotations

from app.models import AnalyzeRequest, TestPlanResponse


MODULE_ZH = {
    "Checkout": "结账流程",
    "Payment Gateway": "支付网关",
    "Order Management": "订单管理",
    "Authentication": "身份认证",
    "Authorization": "权限控制",
    "Backend API": "后端接口",
    "Database": "数据库",
    "Frontend UI": "前端界面",
    "Notification Service": "通知服务",
    "Reporting and Export": "报表与导出",
    "General Application Workflow": "通用应用流程",
}

PROCESS_ZH = {
    "Order-to-cash checkout flow": "从下单到收款的结账流程",
    "Payment authorization and billing": "支付授权与账单",
    "Order lifecycle management": "订单生命周期管理",
    "User access and account security": "用户访问与账号安全",
    "Role-based access control": "基于角色的访问控制",
    "Application service integration": "应用服务集成",
    "Data storage and compatibility": "数据存储与兼容性",
    "User interaction flow": "用户交互流程",
    "Customer and staff communication": "客户与运营通知",
    "Operational reporting": "运营报表",
    "General release validation": "通用发布验证",
}

AREA_ZH = {
    "Commerce workflow": "电商业务流程",
    "External payment integration": "外部支付集成",
    "State transition logic": "状态流转逻辑",
    "Identity and session management": "身份与会话管理",
    "Security policy enforcement": "安全策略执行",
    "Backend API": "后端接口",
    "Persistence layer": "持久化层",
    "Frontend experience": "前端体验",
    "Notification delivery": "通知投递",
    "Reporting service": "报表服务",
    "Application behavior": "应用行为",
}

MODULE_REASON_ZH = {
    "Checkout": "变更触达客户结账路径，需要覆盖主流程、异常恢复和相邻回归场景。",
    "Payment Gateway": "支付行为可能影响收入、重复扣款和失败恢复，需要作为高风险区域验证。",
    "Order Management": "订单状态变化可能影响履约、取消和对账流程。",
    "Authentication": "身份认证变更控制应用访问，需要重点验证安全和会话行为。",
    "Authorization": "权限策略变更可能暴露或阻断受保护操作，需要人工复核。",
    "Backend API": "接口变化可能影响下游消费者，需要验证请求、响应和契约兼容性。",
    "Database": "数据模型变化可能影响兼容性、迁移和恢复路径。",
    "Frontend UI": "界面变化会影响用户完成任务的路径，需要覆盖关键交互。",
    "Notification Service": "通知变化会影响用户和运营人员的可见性。",
    "Reporting and Export": "报表或导出变化可能影响审计、对账和运营流程。",
    "General Application Workflow": "未识别到专门模块关键词，因此按主用户流程做基线验证。",
}

KEYWORD_ZH = {
    "payment": "支付",
    "checkout": "结账",
    "authentication": "身份认证",
    "authorization": "授权",
    "permission": "权限",
    "security": "安全",
    "data deletion": "数据删除",
    "delete": "删除",
    "billing": "账单",
    "invoice": "发票",
    "production": "生产环境",
    "retry": "重试",
    "timeout": "超时",
    "failure": "失败",
    "failed": "失败",
    "order": "订单",
    "database": "数据库",
    "schema": "表结构",
    "api": "接口",
    "integration": "集成",
    "migration": "迁移",
    "ui": "界面",
    "form": "表单",
    "validation": "校验",
    "notification": "通知",
    "email": "邮件",
    "search": "搜索",
    "filter": "筛选",
    "copy": "文案",
    "style": "样式",
    "wording": "措辞",
    "layout": "布局",
}

INPUT_TYPE_ZH = {
    "pr_summary": "PR 摘要",
    "requirement": "产品需求",
    "release_note": "发布说明",
    "bugfix": "缺陷修复",
}


def _zh_keyword_list(text: str) -> str:
    signals = text.replace("Matched signals:", "").strip(" .")
    if not signals:
        return "相关业务信号"
    translated = [KEYWORD_ZH.get(item.strip(), item.strip()) for item in signals.split(",") if item.strip()]
    return "、".join(translated)


def _localize_change(plan: TestPlanResponse, request: AnalyzeRequest, original_modules: list[str]) -> None:
    module_names = [MODULE_ZH.get(module, module) for module in original_modules[:4]]
    module_text = "、".join(module_names) if module_names else "核心应用流程"
    input_type = INPUT_TYPE_ZH.get(request.inputType, request.inputType)
    plan.changeSummary.summary = (
        f"这个{input_type}涉及{module_text}。TestPilot Agent 已将原始变更整理为结构化、基于风险的测试计划，"
        "包括影响范围、风险评分、测试用例、回归建议、人工审批任务和 UiPath 执行方案。"
    )

    if {"Checkout", "Payment Gateway", "Order Management"} & set(original_modules):
        plan.changeSummary.keyChanges = [
            "支付超时后的重试逻辑会影响结账成功率和客户恢复路径。",
            "客户可见错误信息和订单待处理状态需要保持一致。",
            "需要重点防止重复扣款、错误取消订单和失败状态不清晰。",
        ]
    elif {"Authentication", "Authorization"} & set(original_modules):
        plan.changeSummary.keyChanges = [
            "访问控制变更会影响用户能否查看或执行受保护操作。",
            "需要覆盖允许访问、拒绝访问和审计导出路径。",
            "高风险权限变更应由安全或发布负责人复核。",
        ]
    else:
        plan.changeSummary.keyChanges = [
            f"{module_text}受到影响，需要做主流程和相邻回归验证。",
            "生成的测试计划会区分自动化候选、手工检查和人工审批。",
        ]


def _localize_impact(plan: TestPlanResponse) -> None:
    for module in plan.impactAnalysis.affectedModules:
        original_name = module.name
        module.name = MODULE_ZH.get(original_name, original_name)
        module.reason = MODULE_REASON_ZH.get(original_name, module.reason)

    plan.impactAnalysis.businessProcesses = [
        PROCESS_ZH.get(item, item) for item in plan.impactAnalysis.businessProcesses
    ]
    plan.impactAnalysis.technicalAreas = [AREA_ZH.get(item, item) for item in plan.impactAnalysis.technicalAreas]


def _localize_risk(plan: TestPlanResponse) -> None:
    for factor in plan.riskAssessment.riskFactors:
        if "critical business or security keyword" in factor.factor:
            factor.factor = "检测到关键业务或安全信号"
        elif "failure or integration keyword" in factor.factor:
            factor.factor = "检测到失败、超时或集成风险"
        elif "workflow or validation keyword" in factor.factor:
            factor.factor = "检测到流程或校验变化"
        elif "copy or layout keyword" in factor.factor:
            factor.factor = "检测到文案或布局变化"
        elif factor.factor == "Multiple affected modules":
            factor.factor = "影响多个模块"
        elif factor.factor == "General release uncertainty":
            factor.factor = "通用发布不确定性"

        if factor.explanation.startswith("Matched signals:"):
            factor.explanation = f"匹配信号：{_zh_keyword_list(factor.explanation)}。"
        elif "crosses multiple modules" in factor.explanation:
            factor.explanation = "该变更跨多个模块，会提高回归测试和发布编排风险。"
        elif "baseline smoke" in factor.explanation:
            factor.explanation = "即使风险较低，仍需要基线冒烟、功能和回归验证。"


def _localize_tests(plan: TestPlanResponse, original_modules: list[str]) -> None:
    primary = MODULE_ZH.get(original_modules[0], original_modules[0]) if original_modules else "核心流程"
    titles = {
        "TC-001": f"冒烟验证{primary}关键路径",
        "TC-002": f"验证变更行为：{plan.changeSummary.title}",
        "TC-003": f"覆盖{primary}相邻回归场景",
        "TC-004": "验证下游集成契约",
        "TC-005": "探索高风险异常和恢复路径",
        "TC-006": "高风险发布审批门禁",
    }
    steps = {
        "TC-001": [
            "在接近生产的测试环境中打开应用。",
            f"使用有效数据完成主要{primary}流程。",
            "确认用户能够到达预期成功状态，且没有阻塞性错误。",
        ],
        "TC-002": [
            "准备能够触发本次变更行为的测试数据。",
            "执行变更说明中描述的更新路径。",
            "将实际行为与发布需求进行对比。",
        ],
        "TC-003": [
            "运行受影响模块的现有回归场景。",
            "覆盖相邻成功、失败和重试路径。",
            "确认历史支持行为仍然兼容。",
        ],
        "TC-004": [
            "通过公开 API 或集成边界触发变更流程。",
            "检查请求、响应和状态流转数据。",
            "确认依赖服务收到兼容的数据。",
        ],
        "TC-005": [
            "根据风险评估强制触发超时、校验或失败条件。",
            "观察客户可见消息和内部状态更新。",
            "记录需要产品或发布经理复核的行为。",
        ],
        "TC-006": [
            "由 QA Lead 和 Release Manager 复核生成的 P0/P1 用例。",
            "确认自动化和手工门禁是否都已满足。",
            "发布前记录批准或回滚建议。",
        ],
    }
    expected = {
        "TC-001": "主流程在变更后仍然可用。",
        "TC-002": "变更行为符合需求，且不会产生错误状态。",
        "TC-003": "现有支持场景在发布变更后仍然通过。",
        "TC-004": "外部和下游集成与本次变更保持兼容。",
        "TC-005": "异常失败能够被清晰、可恢复地处理。",
        "TC-006": "高风险发布由明确的人类负责人批准或阻止。",
    }

    test_set = f"{primary}发布就绪测试集"
    for test in plan.testCases:
        test.title = titles.get(test.id, test.title)
        test.steps = steps.get(test.id, test.steps)
        test.expectedResult = expected.get(test.id, test.expectedResult)
        test.uipathTestCloudMapping.testSet = test_set
        test.uipathTestCloudMapping.testCaseName = test.title


def _localize_regression(plan: TestPlanResponse) -> None:
    scenario_map = {
        "Cart to payment happy path": ("购物车到支付成功路径", "结账变更可能影响转化路径。"),
        "Coupon and tax calculation": ("优惠券和税费计算", "结账定价规则通常与支付流程相邻。"),
        "Payment failure recovery": ("支付失败恢复", "失败恢复会保护客户信任和订单一致性。"),
        "Authorization timeout and retry": ("授权超时和重试", "网关超时可能造成重复扣款或漏扣。"),
        "Failed payment messaging": ("支付失败提示", "客户需要清晰路径来恢复失败支付。"),
        "Settlement and billing reconciliation": ("结算和账单对账", "支付变更后收入系统必须保持一致。"),
        "Pending order status transition": ("待处理订单状态流转", "订单状态变化会影响履约和客服流程。"),
        "Cancelled order handling": ("取消订单处理", "取消逻辑不能过早触发。"),
        "Core workflow regression": ("核心流程回归", "每个受影响模块都需要基线回归覆盖。"),
    }
    for item in plan.regressionRecommendations:
        original = item.scenario
        item.module = MODULE_ZH.get(item.module, item.module)
        if original in scenario_map:
            item.scenario, item.reason = scenario_map[original]


def _localize_human_review(plan: TestPlanResponse) -> None:
    for task in plan.humanReviewTasks:
        if "QA Lead" in task.title:
            task.title = "QA 负责人审批高风险测试计划"
            task.reason = "生成的计划包含高风险模块或 P0/P1 测试用例，需要人工确认测试范围。"
        elif "Release Manager" in task.title:
            task.title = "发布经理复核收入关键流程"
            task.reason = "结账、支付或订单状态变更可能影响收入和客户恢复路径。"
        elif "Security reviewer" in task.title:
            task.title = "安全负责人审批访问控制变更"
            task.reason = "身份认证和权限变更需要明确的安全复核。"
        elif "Product Owner" in task.title:
            task.title = "产品负责人复核发布就绪状态"
            task.reason = "轻量人工复核可以确认生成的测试范围符合业务预期。"


def _localize_uipath(plan: TestPlanResponse) -> None:
    plan.uipathOrchestrationPlan.summary = (
        "UiPath 作为企业执行和治理层：Test Cloud 管理测试资产，Orchestrator 启动自动化执行，"
        "Action Center 保持人工审批闭环，API Workflows 将发布系统连接到 TestPilot Agent 流程。"
    )
    step_text = {
        1: (
            "接收 GitHub PR 或发布说明输入",
            "从 GitHub、Jira、CI/CD 或手动发布说明表单收集发布上下文。",
            "PR 摘要、需求、发布说明或缺陷修复描述",
            "标准化后的 TestPilot Agent 输入",
        ),
        2: (
            "触发 TestPilot Agent 分析",
            "调用分析流程生成风险、测试用例、回归建议和审批需求。",
            "标准化变更输入",
            "结构化 TestPlanResponse JSON",
        ),
        3: (
            "创建或更新测试资产",
            "将生成的测试用例映射到 Test Cloud 测试集、用例、需求和测试数据。",
            "生成的测试用例",
            "可执行且可追溯的 Test Cloud 资产",
        ),
        4: (
            "启动自动化回归测试",
            "通过无人值守或有人值守机器人运行自动化候选用例。",
            "自动化候选用例",
            "链接回 Test Cloud 的自动化执行结果",
        ),
        5: (
            "分派手工检查和审批任务",
            "将高风险手工检查和审批门禁发送给对应负责人。",
            "手工检查和复核任务",
            "带有复核备注的批准或拒绝决策",
        ),
        6: (
            "生成发布就绪摘要",
            "将 AI 分析、测试执行和人工决策汇总为发布就绪视图。",
            "Test Cloud 结果、Orchestrator 作业状态、Action Center 决策",
            "面向发布干系人的 go / no-go 摘要",
        ),
    }
    for step in plan.uipathOrchestrationPlan.workflowSteps:
        if step.step in step_text:
            step.name, step.description, step.input, step.output = step_text[step.step]

    localized_case_titles = iter(case.title for case in plan.testCases)
    for asset in plan.uipathOrchestrationPlan.testCloudAssets:
        if asset.assetType == "Test Set":
            asset.name = plan.testCases[0].uipathTestCloudMapping.testSet if plan.testCases else "发布就绪测试集"
            asset.description = "按受影响模块和风险分组生成的发布就绪测试集。"
        elif asset.assetType == "Test Case":
            asset.name = next(localized_case_titles, asset.name)
            asset.description = "映射到 UiPath Test Cloud 的测试用例，可作为自动化或手工执行项。"
        elif asset.assetType == "Requirement":
            asset.name = "发布就绪需求"
            asset.description = "将源变更与生成测试覆盖关联起来的可追溯需求项。"


def localize_plan(plan: TestPlanResponse, request: AnalyzeRequest) -> TestPlanResponse:
    if request.language != "zh":
        return plan

    localized = plan.model_copy(deep=True)
    localized.language = "zh"
    original_modules = [module.name for module in localized.impactAnalysis.affectedModules]

    _localize_change(localized, request, original_modules)
    _localize_risk(localized)
    _localize_tests(localized, original_modules)
    _localize_regression(localized)
    _localize_human_review(localized)
    _localize_uipath(localized)
    _localize_impact(localized)
    return localized
