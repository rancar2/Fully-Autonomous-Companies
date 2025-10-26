## 1. Agent Test Cases (Autovalidation Framework)

To ensure the reliability and performance of the autonomous agents, each agent must be self-testable with clear assertions and rollback points. This document outlines a starter test suite for the key agents in the meta-SaaS platform.

---

### ✅ Idea Generator Agent

| Test                    | Input                               | Expected Output                               |
| ----------------------- | ----------------------------------- | --------------------------------------------- |
| Basic prompt            | “Give a B2B SaaS idea for dentists” | Name, problem, persona, and feature outline   |
| Niche collision check   | “CRM for freelancers”               | Reject if 90%+ similarity with prior outputs  |
| Semantic variety        | Prompt 3 times with the same seed   | >= 60% variation in the final output          |

### ✅ Code Scaffolder Agent

| Test             | Input                    | Expected Output                               |
| ---------------- | ------------------------ | --------------------------------------------- |
| CRUD test        | “Build a task manager”   | Scaffold a Rails 8 app with model/controller/view |
| Auth lock        | “Include Devise Turbo”   | Devise included and Turbo integrated          |
| Lint + security  | Generated code           | No RuboCop, Brakeman, or Bun audit issues     |

### ✅ Deployment Agent

| Test          | Trigger              | Expected                                      |
| ------------- | -------------------- | --------------------------------------------- |
| Kamal deploy  | `deploy_to=staging`  | Hetzner IP provisioned, healthcheck returns 200 |
| Rollback test | `deploy_fails=true`  | Revert to the last green commit + notify agents |

---

Each agent logs all test results to `solid_test_results.json` and shares failures with the Meta Orchestrator for retraining or fallback execution.
