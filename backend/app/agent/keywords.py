from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


CRITICAL_KEYWORDS = {
    "payment",
    "checkout",
    "authentication",
    "authorization",
    "permission",
    "security",
    "data deletion",
    "delete",
    "billing",
    "invoice",
    "production",
}

HIGH_KEYWORDS = {
    "retry",
    "timeout",
    "failure",
    "failed",
    "order",
    "database",
    "schema",
    "api",
    "integration",
    "migration",
}

MEDIUM_KEYWORDS = {
    "ui",
    "form",
    "validation",
    "notification",
    "email",
    "search",
    "filter",
}

LOW_KEYWORDS = {
    "copy",
    "style",
    "wording",
    "layout",
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
        keywords=("checkout", "cart", "coupon", "payment", "order"),
        default_level="high",
        business_process="Order-to-cash checkout flow",
        technical_area="Commerce workflow",
        reason="The change touches the customer checkout path.",
    ),
    ModuleRule(
        name="Payment Gateway",
        keywords=("payment", "gateway", "billing", "charge", "authorization", "invoice"),
        default_level="critical",
        business_process="Payment authorization and billing",
        technical_area="External payment integration",
        reason="Payment behavior can affect revenue, duplicate charges, and failed recovery.",
    ),
    ModuleRule(
        name="Order Management",
        keywords=("order", "fulfillment", "status", "pending", "cancelled"),
        default_level="high",
        business_process="Order lifecycle management",
        technical_area="State transition logic",
        reason="Order status changes can break fulfillment or reconciliation flows.",
    ),
    ModuleRule(
        name="Authentication",
        keywords=("login", "auth", "authentication", "session", "password"),
        default_level="critical",
        business_process="User access and account security",
        technical_area="Identity and session management",
        reason="Authentication changes control access to the application.",
    ),
    ModuleRule(
        name="Authorization",
        keywords=("authorization", "permission", "role", "policy", "access"),
        default_level="critical",
        business_process="Role-based access control",
        technical_area="Security policy enforcement",
        reason="Permission changes can expose or block protected workflows.",
    ),
    ModuleRule(
        name="Backend API",
        keywords=("api", "endpoint", "request", "response", "contract"),
        default_level="high",
        business_process="Application service integration",
        technical_area="Backend API",
        reason="API changes can affect multiple downstream consumers.",
    ),
    ModuleRule(
        name="Database",
        keywords=("database", "schema", "migration", "table", "column"),
        default_level="high",
        business_process="Data storage and compatibility",
        technical_area="Persistence layer",
        reason="Data model changes can affect compatibility and recovery.",
    ),
    ModuleRule(
        name="Frontend UI",
        keywords=("ui", "page", "button", "form", "layout", "message"),
        default_level="medium",
        business_process="User interaction flow",
        technical_area="Frontend experience",
        reason="UI changes can alter how users complete the workflow.",
    ),
    ModuleRule(
        name="Notification Service",
        keywords=("notification", "email", "sms", "alert"),
        default_level="medium",
        business_process="Customer and staff communication",
        technical_area="Notification delivery",
        reason="Notification changes can affect operational visibility.",
    ),
    ModuleRule(
        name="Reporting and Export",
        keywords=("report", "export", "download", "csv", "pdf"),
        default_level="medium",
        business_process="Operational reporting",
        technical_area="Reporting service",
        reason="Reporting changes can affect audit and compliance workflows.",
    ),
)


def contains_any(text: str, keywords: Iterable[str]) -> list[str]:
    lower = text.lower()
    return [keyword for keyword in keywords if keyword.lower() in lower]
