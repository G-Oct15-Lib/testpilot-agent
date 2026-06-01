from __future__ import annotations

from app.models import ImpactAnalysis, RegressionRecommendation


REGRESSION_LIBRARY = {
    "Checkout": [
        ("Cart to payment happy path", "Checkout changes can affect the conversion path."),
        ("Coupon and tax calculation", "Checkout pricing rules are often adjacent to payment flow."),
        ("Payment failure recovery", "Failure recovery protects customer trust and order consistency."),
    ],
    "Payment Gateway": [
        ("Authorization timeout and retry", "Gateway timeouts can create duplicate or missing charges."),
        ("Failed payment messaging", "Customers need a clear path to recover from failed payments."),
        ("Settlement and billing reconciliation", "Revenue systems must stay consistent after payment changes."),
    ],
    "Order Management": [
        ("Pending order status transition", "Order status changes affect fulfillment and support workflows."),
        ("Cancelled order handling", "Cancellation logic must not trigger prematurely."),
    ],
    "Authentication": [
        ("Login and logout regression", "Access changes can break basic account flows."),
        ("Session expiry handling", "Session behavior must remain secure and predictable."),
    ],
    "Authorization": [
        ("Role permission matrix", "Permission changes can expose protected actions."),
        ("Access denied path", "Blocked access should fail clearly and safely."),
    ],
    "Backend API": [
        ("API contract compatibility", "Downstream consumers need stable request and response shapes."),
        ("Error response compatibility", "Clients depend on predictable error formats."),
    ],
    "Database": [
        ("Migration rollback path", "Schema changes need recovery coverage."),
        ("Data compatibility check", "Existing records must remain readable and valid."),
    ],
}


def recommend_regression(impact: ImpactAnalysis) -> list[RegressionRecommendation]:
    recommendations: list[RegressionRecommendation] = []
    for module in impact.affectedModules:
        scenarios = REGRESSION_LIBRARY.get(
            module.name,
            [("Core workflow regression", "Every affected module needs baseline regression coverage.")],
        )
        for scenario, reason in scenarios:
            priority = "P0" if module.impactLevel == "critical" else "P1" if module.impactLevel == "high" else "P2"
            recommendations.append(
                RegressionRecommendation(
                    module=module.name,
                    scenario=scenario,
                    reason=reason,
                    priority=priority,  # type: ignore[arg-type]
                )
            )
    return recommendations[:8]

