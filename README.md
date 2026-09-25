# Enterprise GitHub Platform & CI/CD Masterclass
> **Production-Grade Workflow Automation, Composite Actions, Matrix Strategies & AI Governance Patterns**

This repository serves as a real-world reference implementation for **Senior GitHub Platform Engineers**, **DevOps Architects**, and **Platform Engineering Teams**. It demonstrates enterprise CI/CD patterns designed for scalability, governance, security, and developer productivity.

---

## 🏛️ Repository Architecture

```
enterprise-github-workflows/
├── .github/
│   ├── actions/
│   │   └── setup-app-env/              # 1. COMPOSITE ACTION (Reusable step bundle)
│   │       └── action.yml
│   ├── copilot-instructions.md         # 2. AI GOVERNANCE (Copilot Enterprise custom context)
│   └── workflows/
│       ├── reusable-ci.yml             # 3. REUSABLE WORKFLOW (workflow_call with inputs/secrets)
│       ├── matrix-strategy-advanced.yml# 4. ADVANCED MATRIX (include, exclude, fail-fast, max-parallel)
│       ├── dynamic-matrix.yml          # 5. DYNAMIC RUNTIME MATRIX (fromJson calculation)
│       └── main-app-pipeline.yml       # 6. ORCHESTRATION PIPELINE (Caller + Concurrency)
├── app/                                # Sample Microservice (Ticket Processor)
│   └── main.py
├── tests/                              # Pytest Unit Test Suite
│   └── test_main.py
├── requirements.txt                    # Runtime dependencies
└── README.md                           # Documentation & Interview Guide
```

---

## 🚀 Key Patterns Explained

### 1. Composite Actions (`.github/actions/setup-app-env`)
* **What it is:** A reusable bundle of multiple workflow steps grouped into a single custom action.
* **When to use:** When multiple jobs/workflows need to repeat identical sequential steps (e.g., setting up Python, configuring pip caching, installing CLI tools).
* **Key Features in this repo:**
  * Defines clean `inputs` with defaults (`python-version`, `enable-cache`).
  * Employs `actions/cache@v4` with dynamic hash keys (`hashFiles('requirements.txt')`).
  * Exports `outputs` (`version`, `cache-hit`) back to the calling workflow.

---

### 2. Reusable Workflows (`.github/workflows/reusable-ci.yml`)
* **What it is:** A complete, self-contained workflow triggered via `on: workflow_call`.
* **When to use:** Standardizing complete CI/CD pipelines across 100+ repositories (The "Golden Path").
* **Key Features in this repo:**
  * Strict input typing (`type: boolean`, `type: string`).
  * Conditional gate execution (`if: ${{ inputs.run-linter == true }}`).
  * Secure secret handling (`secrets: { SONAR_TOKEN: { required: false } }`).
  * Exports structured telemetry outputs (`test-outcome`, `coverage-score`) for downstream release gates.

---

### 3. Advanced Matrix Strategy (`.github/workflows/matrix-strategy-advanced.yml`)
* **What it is:** Multi-dimensional testing across operating systems and runtime versions with enterprise throttling.
* **Critical Parameters:**
  * **`fail-fast: false`**: By default, GitHub kills all running jobs if any single matrix job fails. Setting this to `false` ensures you get the full diagnostic matrix across all platforms.
  * **`max-parallel: 4`**: Prevents runner starvation by capping concurrent runner consumption.
  * **`exclude`**: Skips deprecated or incompatible combinations (e.g., skips `windows-latest` + `python 3.10`).
  * **`include`**: Injects custom attributes (e.g., marking Ubuntu + Python 3.12 as `experimental: true`) or adds a new platform (e.g., `macos-latest`).

---

### 4. Dynamic Matrix Strategy (`.github/workflows/dynamic-matrix.yml`)
* **What it is:** A two-stage pipeline where the matrix is not hardcoded, but calculated dynamically at runtime.
* **How it works:**
  * **Stage 1 (Generator):** Inspects changed files, Git diffs, or service tiers and emits a JSON payload string to `$GITHUB_OUTPUT`.
  * **Stage 2 (Worker):** Consumes the matrix dynamically using `${{ fromJson(needs.generator.outputs.matrix) }}`.
* **Enterprise Use Case:** Monorepos with 50+ microservices where only services modified in the current pull request should be built and tested.

---

### 5. Orchestration & Concurrency (`.github/workflows/main-app-pipeline.yml`)
* **What it is:** A caller workflow invoking the reusable CI template and managing release gating.
* **Concurrency Control:**
  ```yaml
  concurrency:
    group: ${{ github.workflow }}-${{ github.ref }}
    cancel-in-progress: true
  ```
  * Cancels outdated running builds when a developer rapidly pushes new commits to the same PR, conserving compute minutes.

---

### 6. AI Governance (`.github/copilot-instructions.md`)
* Enforces team-wide coding conventions, security rules, and linting standards directly into GitHub Copilot Chat and CLI suggestions.
* Ensures **Zero AI-Induced Production Defects** by mandating automated PR validation before merge.

---

## 🎯 Interview Quick Reference Cheat Sheet

| Feature | Composite Action | Reusable Workflow (`workflow_call`) |
| :--- | :--- | :--- |
| **Scope** | Step-level reuse | Full Job / Pipeline reuse |
| **Runners** | Runs inside caller's runner environment | Can specify its own `runs-on` runners |
| **Secrets** | Must be passed as inputs or inherited | Explicitly declared under `secrets:` |
| **Multiple Jobs** | No (steps only) | Yes (can orchestrate multi-job graphs) |
| **Ideal For** | Environment setup, tool install, caching | Enterprise standard CI/CD "Golden Paths" |

---

## 🛠️ Testing Locally
```bash
# Install dependencies
pip install -r requirements.txt

# Run pytest unit tests
pytest -v tests/

# Run flake8 linter
flake8 app/ tests/
```
