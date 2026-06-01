# Demo Script

This script is designed for a 5-7 minute UiPath AgentHack demo. It assumes the app is running in local mock mode and does not require live UiPath credentials.

## Demo Goal

Show how TestPilot Agent turns a release change into a structured UiPath-ready testing plan:

- What changed?
- What modules are impacted?
- How risky is the release?
- What should be tested?
- What needs human review?
- How would UiPath Test Cloud, Orchestrator, Action Center, Apps, Integration Service, and API Workflows fit?

## Demo Persona

Primary persona: enterprise release manager or QA lead.

Supporting personas:

- Developer submitting a pull request.
- QA engineer reviewing generated test cases.
- Business SME approving high-risk release impact.
- Automation engineer mapping tests to UiPath execution.

## Sample Input

Use a business process that feels natural for UiPath: invoice approval, onboarding, claims processing, purchase order routing, or customer support escalation.

Suggested sample:

```text
Title: Fix delegated manager routing in invoice approval

Bugfix summary:
Invoices above $25,000 were incorrectly routed to the original manager when
the assigned approver was on leave. This change updates the approval routing
logic to use delegated manager rules, adds an exception path for expired
delegations, and updates the audit note shown to finance operations.

Acceptance criteria:
- If the assigned manager has an active delegate, route approval to the delegate.
- If delegation is expired, route to finance operations queue.
- Preserve audit history for original manager, delegate, and timestamp.
- Do not change routing for invoices below $25,000.
```

## Talk Track

### 1. Open with the Release Problem

Say:

"Enterprise release teams often receive a PR, a bugfix note, or a Jira story and then need to manually decide what changed, what is risky, what to test, and who needs to review it. TestPilot Agent compresses that planning step into a structured, reviewable workflow for UiPath Test Cloud."

Show:

- The input panel.
- The example release text.
- The local mock mode label, if available.

### 2. Submit the Release Input

Action:

- Paste or select the sample input.
- Run the analysis.

Say:

"For the hackathon MVP, this runs locally with mock UiPath adapters. The product boundary is realistic: we generate the same objects we would send to Test Cloud, Orchestrator, Action Center, Apps, Integration Service, and API Workflows."

Expected result:

- Change summary appears.
- Impacted modules appear.
- Risk score appears.
- Test cases and regression recommendations appear.

### 3. Explain the Change Summary and Impact

Point out:

- Business process: invoice approval.
- Impacted modules: approval routing, delegation rules, finance operations queue, audit history.
- Impacted users: manager, delegate approver, finance operations.
- Impacted test assets: workflow tests, regression tests, audit validation, boundary tests around invoice amount.

Say:

"The agent does not just paraphrase the release note. It turns the change into a testing map: business capability, technical surface, user roles, and affected test coverage."

### 4. Explain the Risk Score

Point out:

- Medium or high score depending on the app's output.
- Rationale: approval routing, financial threshold, audit trail, exception path, delegated approval.

Say:

"The score is explainable. A finance workflow with audit impact should not be treated like a low-risk UI copy change. This is where release teams can tune policy thresholds."

Suggested risk framing:

- Low risk: standard smoke tests.
- Medium risk: targeted regression and QA sign-off.
- High risk: expanded regression, business review, and release approval task.

### 5. Review Generated Test Cases

Point out test cases such as:

- Active delegate receives approval for invoice above threshold.
- Expired delegation routes to finance operations queue.
- Invoice below threshold keeps existing routing.
- Audit history captures original manager, delegate, timestamp, and exception reason.
- Negative test for missing delegate record.

Say:

"Each generated test is structured enough to become a draft in UiPath Test Cloud: objective, preconditions, test data, steps, expected results, priority, and automation suitability."

### 6. Show Regression Recommendations

Point out:

- Required smoke suite.
- Targeted regression for invoice routing.
- Audit trail validation.
- Role and permission checks.
- Optional exploratory testing for edge cases.

Say:

"The regression plan is scoped by impact and risk. That helps avoid both under-testing high-risk changes and over-testing every release."

### 7. Show Human Review Tasks

Point out:

- Business owner review for approval routing.
- Finance operations review for exception queue behavior.
- Compliance or audit review if risk is high.

Say:

"This is where UiPath Action Center fits. The agent should not silently approve sensitive workflow changes. It creates human-in-the-loop tasks when the context is risky or ambiguous."

### 8. Show the UiPath Integration Plan

Walk through each platform role:

- Test Cloud: draft test cases and test sets.
- Orchestrator: queue automated regression jobs.
- Action Center: create review and approval tasks.
- Apps: provide the release testing cockpit.
- Integration Service: connect GitHub, Jira, ServiceNow, Teams, or Slack.
- API Workflows: wrap cross-system operations like creating tests, queueing jobs, and posting notifications.

Say:

"The MVP is mock-first, but the integration boundaries are explicit. A UiPath team can replace the mock adapters with real tenant calls without changing the core release planning flow."

### 9. Close with the Codex Angle

Say:

"Codex helped build this as a coding agent: shaping the architecture, generating implementation scaffolds, preparing tests and documentation, and keeping the project aligned with the hackathon story. That matters because this product is itself about AI-assisted software delivery and quality control."

## Backup Demo Path

If the live app has issues, use this fallback:

1. Show the sample input.
2. Open a saved mock response or screenshot.
3. Walk through the generated sections in order: summary, impact, risk, tests, regression, review tasks, UiPath plan.
4. Emphasize the integration architecture rather than live API calls.

## Judge Q&A Preparation

### Why does this use mock UiPath adapters?

The MVP focuses on the agent workflow and avoids requiring hackathon judges to provide tenant credentials. The adapters make the production integration path explicit and reduce demo fragility.

### How does this relate to UiPath Test Cloud?

Test Cloud is the quality hub. TestPilot Agent generates draft test cases, recommends test sets, explains coverage, and prepares execution context that can be pushed into Test Cloud.

### Where does Orchestrator fit?

Orchestrator runs the automation jobs for recommended regression and smoke suites. TestPilot Agent plans which jobs should run and with what release parameters.

### Why is Action Center important?

High-risk release decisions need human accountability. Action Center is the natural place to assign review, clarification, and approval tasks.

### How is this different from a chatbot?

The product outputs structured release testing artifacts, not just a conversational answer. It produces risk scoring, test cases, regression scope, review tasks, and integration actions that map to UiPath systems.

### What would production hardening require?

Tenant authentication, secure secret storage, source system connectors, API workflows, audit logging, role-based access, observability, retry handling, and policy thresholds for release gates.

## Suggested Demo Timing

| Time | Segment |
| --- | --- |
| 0:00-0:45 | Problem and persona |
| 0:45-1:30 | Submit release input |
| 1:30-2:30 | Summary, impact, and risk |
| 2:30-3:45 | Test cases and regression plan |
| 3:45-4:45 | Human review tasks |
| 4:45-6:00 | UiPath integration plan |
| 6:00-7:00 | Codex development angle and close |
