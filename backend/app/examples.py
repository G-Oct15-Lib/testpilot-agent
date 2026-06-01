from __future__ import annotations

from app.models import ExampleScenario


EXAMPLES = [
    ExampleScenario(
        id="checkout-payment-risk",
        title="Checkout payment timeout handling",
        inputType="pr_summary",
        businessContext="E-commerce checkout and payment workflow",
        content="""PR Summary: Checkout payment timeout handling
This PR updates the checkout payment retry logic. When the payment gateway times out, the system now retries the authorization request up to two times before marking the payment as failed. It also changes the error message shown to the customer and updates order status handling so that pending payments are not immediately cancelled.

Changed areas:
- Checkout payment flow
- Payment gateway adapter
- Order status update logic
- Customer-facing error message

Potential concern:
This affects the revenue-critical checkout path and may impact order creation, duplicate charges, and failed payment recovery.""",
    ),
    ExampleScenario(
        id="auth-role-policy",
        title="Role permission policy update",
        inputType="requirement",
        businessContext="Enterprise admin portal authorization workflow",
        content="""The admin portal now supports a delegated support role. Support agents can view customer account details and export audit notes, but they cannot update billing settings, delete users, or change security policies. The change updates permission checks across the account profile page, API endpoints, and audit export flow.""",
    ),
    ExampleScenario(
        id="invoice-export-bugfix",
        title="Invoice export timeout bugfix",
        inputType="bugfix",
        businessContext="Finance reporting and invoice reconciliation",
        content="""A bugfix changes the invoice export job to stream large CSV files instead of loading the full report into memory. It touches the reporting API, invoice query, and download status notification. The fix should reduce timeout failures for enterprise accounts with high invoice volume.""",
    ),
]

