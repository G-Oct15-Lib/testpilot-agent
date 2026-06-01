from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


CRITICAL_KEYWORDS = {
    "payment",
    "付款",
    "支付",
    "checkout",
    "结账",
    "收银台",
    "authentication",
    "认证",
    "authorization",
    "授权",
    "permission",
    "权限",
    "security",
    "安全",
    "data deletion",
    "delete",
    "删除",
    "billing",
    "账单",
    "invoice",
    "发票",
    "production",
    "生产",
}

HIGH_KEYWORDS = {
    "retry",
    "重试",
    "timeout",
    "超时",
    "failure",
    "failed",
    "失败",
    "order",
    "订单",
    "database",
    "数据库",
    "schema",
    "表结构",
    "api",
    "integration",
    "集成",
    "migration",
    "迁移",
}

MEDIUM_KEYWORDS = {
    "ui",
    "界面",
    "form",
    "表单",
    "validation",
    "校验",
    "notification",
    "通知",
    "email",
    "邮件",
    "search",
    "搜索",
    "filter",
    "筛选",
}

LOW_KEYWORDS = {
    "copy",
    "文案",
    "style",
    "样式",
    "wording",
    "措辞",
    "layout",
    "布局",
}


@dataclass(frozen=True)
class ModuleRule:
    name: str
    keywords: tuple[str, ...]
    default_level: str
    business_process: str
    technical_area: str
    reason: str


MODULE_RULES = (
    ModuleRule(
        name="Checkout",
        keywords=("checkout", "cart", "coupon", "payment", "order", "结账", "购物车", "优惠券", "支付", "付款", "订单"),
        default_level="high",
        business_process="Order-to-cash checkout flow",
        technical_area="Commerce workflow",
        reason="The change touches the customer checkout path.",
    ),
    ModuleRule(
        name="Payment Gateway",
        keywords=("payment", "gateway", "billing", "charge", "authorization", "invoice", "支付", "付款", "网关", "账单", "扣款", "授权", "发票"),
        default_level="critical",
        business_process="Payment authorization and billing",
        technical_area="External payment integration",
        reason="Payment behavior can affect revenue, duplicate charges, and failed recovery.",
    ),
    ModuleRule(
        name="Order Management",
        keywords=("order", "fulfillment", "status", "pending", "cancelled", "订单", "履约", "状态", "待处理", "取消"),
        default_level="high",
        business_process="Order lifecycle management",
        technical_area="State transition logic",
        reason="Order status changes can break fulfillment or reconciliation flows.",
    ),
    ModuleRule(
        name="Authentication",
        keywords=("login", "auth", "authentication", "session", "password", "登录", "认证", "会话", "密码"),
        default_level="critical",
        business_process="User access and account security",
        technical_area="Identity and session management",
        reason="Authentication changes control access to the application.",
    ),
    ModuleRule(
        name="Authorization",
        keywords=("authorization", "permission", "role", "policy", "access", "授权", "权限", "角色", "策略", "访问"),
        default_level="critical",
        business_process="Role-based access control",
        technical_area="Security policy enforcement",
        reason="Permission changes can expose or block protected workflows.",
    ),
    ModuleRule(
        name="Backend API",
        keywords=("api", "endpoint", "request", "response", "contract", "接口", "端点", "请求", "响应", "契约"),
        default_level="high",
        business_process="Application service integration",
        technical_area="Backend API",
        reason="API changes can affect multiple downstream consumers.",
    ),
    ModuleRule(
        name="Database",
        keywords=("database", "schema", "migration", "table", "column", "数据库", "表结构", "迁移", "表", "字段"),
        default_level="high",
        business_process="Data storage and compatibility",
        technical_area="Persistence layer",
        reason="Data model changes can affect compatibility and recovery.",
    ),
    ModuleRule(
        name="Frontend UI",
        keywords=("ui", "page", "button", "form", "layout", "message", "界面", "页面", "按钮", "表单", "布局", "消息", "文案"),
        default_level="medium",
        business_process="User interaction flow",
        technical_area="Frontend experience",
        reason="UI changes can alter how users complete the workflow.",
    ),
    ModuleRule(
        name="Notification Service",
        keywords=("notification", "email", "sms", "alert", "通知", "邮件", "短信", "提醒"),
        default_level="medium",
        business_process="Customer and staff communication",
        technical_area="Notification delivery",
        reason="Notification changes can affect operational visibility.",
    ),
    ModuleRule(
        name="Reporting and Export",
        keywords=("report", "export", "download", "csv", "pdf", "报表", "导出", "下载"),
        default_level="medium",
        business_process="Operational reporting",
        technical_area="Reporting service",
        reason="Reporting changes can affect audit and compliance workflows.",
    ),
)


def contains_any(text: str, keywords: Iterable[str]) -> list[str]:
    lower = text.lower()
    return [keyword for keyword in keywords if keyword.lower() in lower]
