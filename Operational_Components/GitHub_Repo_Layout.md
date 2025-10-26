## 6. GitHub Repo & File Layout (Fortified)

This document outlines the 100x-detailed GitHub repository layout for the autonomous meta-SaaS business, updated to reflect the Fortified Strategy.

---

### 📦 `meta-saas/` – Root Directory

The root of the project, containing all the code and documentation for the fully agent-operated, multi-tenant SaaS launcher.

### 🗂️ Top-Level Structure

```
meta-saas/
├── agents/                   # Agent definitions & prompts
├── memory/                   # Persistent memory, summaries, reflections
├── mvp_saas/                 # Current live SaaS business (single-tenant view)
├── engine/                   # Core autonomous orchestration logic
├── api/                      # OpenAPI schema + FastAPI/Bun endpoints
├── ui/                       # Meta control panel frontend (Tailwind + HTMX or Bun + React)
├── data/                     # Datasets, evaluation logs, user feedback
├── tests/                    # Automated testing for agent workflows
├── ops/                      # Kamal deploy configs, .env, secrets
├── scripts/                  # One-off scripts: bootstrapping, analysis, etc.
├── docs/                     # Markdown knowledge base
├── .github/                  # Workflows, issue templates, PR bots
├── meta/                     # Logs, architecture, governance
├── legal/                    # Legal documents (e.g., Terms of Service)
├── db_schema.md              # Database schema definitions
├── financial_model.md        # Financial model and projections
└── README.md                 # Project overview
```

### 🧠 `agents/` – Agent Source & Prompt Logic

Each agent is a modular plug-in with its own version-controlled directory containing its prompt, memory, and dynamic strategy configurations.

```
agents/
├── ceo_agent/
│   └── prompt.txt
├── cfo_agent/
│   └── prompt.txt
├── cto_agent/
│   └── prompt.txt
├── guardian_agent/
│   └── prompt.txt
├── auditor_agent/
│   └── prompt.txt
├── code_quality_agent/
│   └── prompt.txt
├── idea_generator_agent/
│   └── prompt.txt
├── market_validator_agent/
│   └── prompt.txt
├── coder_agent/
│   └── prompt.txt
├── deployer_agent/
│   └── prompt.txt
├── marketer_agent/
│   └── prompt.txt
├── billing_agent/
│   └── prompt.txt
├── customer_support_agent/
│   └── prompt.txt
├── evaluator_agent/
│   └── prompt.txt
└── __init__.py               # Agent loader
```

### 🧠 `memory/` – Long-Term Learning

This directory contains the components that feed the weekly agent digestion and architecture refinement.

```
memory/
├── logs.sqlite                # Core task log + embedding index
├── vector_store.bin          # Top-k memory compression
├── summaries/
│   ├── deploy-1-week-28.md
│   └── scaffold-1-week-28.md
└── feedback/
    ├── user_1_thumbsdown.json
    └── anomaly_reports.json
```

### 🚀 `mvp_saas/` – The Currently Live SaaS Business

This folder acts as a mounted live instance of a SaaS product. In the future, this will be expanded to support multi-tenant deployments or a split-repo model (`saas_001/`, `saas_002/`, etc.).

```
mvp_saas/
├── saas_config.yml           # Configuration for the current SaaS
├── app/
│   ├── models/
│   ├── controllers/
│   └── views/
├── db/
│   ├── schema.sql
│   └── seeds.rb
└── billing/
    └── stripe.rb
```

### 🔁 `engine/` – Agent Looping & Scheduler Logic

This directory implements the LangGraph or CrewAI graph logic that drives each agentic task.

```
engine/
├── orchestrator.rb           # Agent loop executor
├── base_agent.rb             # Base class for all agents
├── scheduler.rb              # Daily/weekly planner
├── goal_stack.rb             # Long-term memory + goal prioritizer
├── health_checker.rb         # Watchdog for failures
└── memory_refresher.rb       # Vector prune + summarizer
```

### 🌐 `api/` – Public + Internal Meta Endpoints

Built with an OpenAPI-first design so that agents can consume their own APIs.

```
api/
├── meta_openapi.yaml         # Exposes endpoints like "create new SaaS" and "audit agent memory"
├── routes/
│   ├── index.rb
│   ├── meta_stats.rb
│   └── saas_lifecycle.rb
└── tests/
    └── api_contract_spec.rb
```

### 🤖 `.github/` – GitOps Meta Layer

Agents are triggered by GitHub Actions, which can be initiated by `cron`, a `file change`, or a `command input`.

```
.github/
├── workflows/
│   ├── run_agents.yml
│   ├── agent_self_update.yml
│   └── test_memory_loop.yml
├── ISSUE_TEMPLATE/
├── PULL_REQUEST_TEMPLATE.md
└── CODEOWNERS
```
