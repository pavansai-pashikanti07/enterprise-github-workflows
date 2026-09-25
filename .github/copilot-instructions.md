# GitHub Copilot Enterprise Instructions & Governance

## Project Architecture & Engineering Standards
This repository adheres to enterprise platform engineering and CI/CD governance best practices.

### 1. Workflow & Action Guidelines
- **Composite Actions:** Always define inputs with clear descriptions, default values, and explicit `shell: bash` on step definitions.
- **Reusable Workflows:** Always use `on: workflow_call:` with strict type checking for inputs (string, boolean, number) and export key telemetry via `outputs:`.
- **Security & Secrets:** Never hardcode credentials. Use short-lived OIDC tokens for AWS/Azure integrations. Never output plain-text secrets in step logs.
- **Concurrency:** Ensure `concurrency` groups with `cancel-in-progress: true` are configured on PR workflows to conserve runner minutes.

### 2. Python Code Standards
- Adhere strictly to PEP 8 standards enforced via `flake8`.
- Write unit tests using `pytest` for every utility function with clear assertion messages.
- Avoid external dependencies where Python standard library suffices.

### 3. AI Code Review & Zero-Defect Rule
- AI-generated code must pass static analysis (`flake8`) and unit test gates prior to merge consideration.
- Hallucinated package imports or deprecated action versions (e.g. `actions/checkout@v2`) are strictly prohibited.
